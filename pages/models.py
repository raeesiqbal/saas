from django.db import models

ACTIVE = (
    ("yes", "Yes"),
    ("no", "No"),
)


class Record(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    similarity_score = models.FloatField()
    active = models.CharField(max_length=5, choices=ACTIVE, default="yes")
    date = models.DateField()
    date_posted = models.DateField(auto_now=True)
