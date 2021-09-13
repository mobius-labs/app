from enum import Enum
from django.db import models

from apps.account_page.models import User


class EventTag(Enum):
    BUS = "business"
    FRN = "friend"
    FAM = "family"
    PER = "personal"
    OTH = "other"


class EventResponse(Enum):
    GOI = "going"
    TEN = "tentative"
    DEC = "declined"


class Event(models.Model):

    event_id = models.IntegerField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=45)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    is_all_day = models.BooleanField()
    location = models.CharField(max_length=45, null=True)
    notes = models.TextField(null=True)
    url = models.CharField(max_length=45, null=True)
    tag = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in EventTag]
    )
    response = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in EventResponse]
    )
    is_public = models.BooleanField()
    alert = models.DateTimeField(null=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)


class EventOccurrence(models.Model):

    date = models.DateTimeField(primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, primary_key=True)


class EventIncludesContact(models.Model):

    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)


