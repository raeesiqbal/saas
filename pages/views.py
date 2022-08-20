from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import Record
from django.db.models import Q
import stripe
from mysite.stripe_key import SECRET_KEY

stripe.api_key = SECRET_KEY


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "pages/home.html", context=context)


class RecordsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_authenticated is True:
            get_records = Record.objects.order_by("-date_posted")
            context = {
                "records": get_records,
            }
            return render(request, "pages/record.html", context=context)
        return redirect("users:logout")


class RecordDetailView(View):
    def get(self, request, id, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_authenticated is True:
            get_record = Record.objects.get(id=id)
            context = {
                "record": get_record,
            }
            return render(request, "pages/record-detail.html", context=context)
        return redirect("users:logout")


class SearchView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_authenticated is True:
            return redirect("pages:records")
        return redirect("users:logout")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_authenticated is True:
            print(request.POST)
            text = request.POST["search_text"]
            active = False
            inactive = False
            by_time = request.POST["by_time"]
            by_score = request.POST["by_score"]
            range = request.POST["range"]
            if range:
                range = range.split("to")
                start_date = range[0].replace(" ", "")
                end_date = range[1].replace(" ", "")
            if "active" in request.POST:
                active = True
            if "inactive" in request.POST:
                inactive = True
            if text is not "":
                results = Record.objects.filter(
                    Q(title__icontains=text) | Q(description__icontains=text)
                )
            else:
                results = Record.objects.all()
            if active and inactive or active is False and inactive is False:
                results = results.filter(Q(active="yes") | Q(active="no"))
            if active is True and inactive is False:
                results = results.filter(active="yes")
            if active is False and inactive is True:
                results = results.filter(active="no")
            if range is "":
                results = results
            else:
                results = results.filter(date__range=[start_date, end_date])
            if by_time == "recent":
                results = results.order_by("-date")
            if by_time == "oldest":
                results = results.order_by("date")
            if by_score == "high":
                results = results.order_by("-similarity_score")
            if by_score is "low":
                results = results.order_by("similarity_score")
            context = {
                "records": results,
                "active": active,
                "inactive": inactive,
                "range": request.POST["range"],
                "by_time": by_time,
                "by_score": by_score,
            }
            return render(request, "pages/record.html", context=context)
        return redirect("users:logout")
