from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from .forms import *
from .models import *
import stripe
from django.contrib import messages
from mysite.stripe_key import SECRET_KEY
from django.views.decorators.csrf import csrf_exempt

key = "whsec_40aed4e9f99ac951e1c40acd20f2cd4cccefe9460ba8f675011a996230861ba8"
stripe.api_key = SECRET_KEY


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": BaseSignupForm(),
        }
        return render(request, "users/register.html", context=context)

    def post(self, request, *args, **kwargs):
        user_form = BaseSignupForm(request.POST)
        context = {
            "form": user_form,
        }
        if user_form.is_valid():
            user_form.save()
            user = authenticate(
                request,
                username=request.POST["email"],
                password=request.POST["password1"],
            )
            login(request, user)
            return redirect("pages:home")
        messages.error(request, "Please remove the form errors.")
        return render(request, "users/register.html", context=context)


class AccountSettingView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {"form": BaseEditForm(instance=request.user)}
            return render(request, "users/account-settings.html", context=context)
        return redirect("login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = BaseEditForm(request.POST, instance=request.user)
            context = {
                "form": form,
            }
            if form.is_valid():
                form.save()
                messages.success(request, "Account is updated successfully.")
            messages.error(request, "Please remove the form errors.")
            return render(request, "users/account-settings.html", context=context)
        return redirect("login")


class PasswordChangeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {
                "form": UserPasswordChangeForm(self.request.user),
            }
            return render(request, "users/password-reset.html", context=context)
        return redirect("users:login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserPasswordChangeForm(request.user, request.POST)
            context = {
                "form": form,
            }
            if form.is_valid():
                form.save()
                messages.success(request, "Password is changed successfully.")
                update_session_auth_hash(self.request, form.user)
            messages.error(request, "Please remove the form errors.", "error")
            return render(request, "users/password-reset.html", context=context)
        return redirect("login")


@csrf_exempt
def Webhook(request):
    if request.method == "POST":
        event = None
        payload = request.body
        sig_header = request.headers["STRIPE_SIGNATURE"]
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, key)
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e
        # Handle the event

        # if event["type"] == "invoice.paid":
        #     get_user.subscribed = True
        #     get_user.save()

        if event["type"] == "invoice.created":
            return JsonResponse(status=200, data={"status": "success"})

        if event["type"] == "customer.subscription.deleted":
            get_user = CustomUser.objects.filter(
                subscription_id=event["data"]["object"]["id"]
            ).first()
            get_user.stripe_id = None
            get_user.subscribed = False
            get_user.subscription_id = None
            get_user.subscription_amount = None
            get_user.subscription_interval = None
            get_user.save()

        if event["type"] == "checkout.session.completed":
            get_user = CustomUser.objects.filter(
                id=event["data"]["object"]["client_reference_id"]
            ).first()
            if event["data"]["object"]["payment_status"] == "paid":
                if get_user.subscribed is False:
                    get_user.subscribed = True
                    get_user.stripe_id = event["data"]["object"]["customer"]
                    get_user.subscription_id = event["data"]["object"]["subscription"]
                    get_subscription = stripe.Subscription.retrieve(
                        event["data"]["object"]["subscription"],
                    )
                    get_user.subscription_amount = (
                        get_subscription["items"]["data"][0]["plan"]["amount"] / 100
                    )
                    get_user.subscription_interval = get_subscription["items"]["data"][
                        0
                    ]["plan"]["interval"]
                    get_user.save()

        return JsonResponse(status=200, data={"status": "success"})


class StripeCustomerPortalView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session = stripe.billing_portal.Session.create(
                customer=request.user.stripe_id,
                return_url="https://example.com/account",
            )
            return redirect(session.url)
        return redirect("users:login")
