from enum import Enum
from django.db import models

from apps.account.models import User
from apps.contact_book.models import Contact


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
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE)


class EventOccurrence(models.Model):

    event_occurrence_id = models.IntegerField(auto_created=True, primary_key=True)
    date = models.DateTimeField()
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


class EventIncludesContact(models.Model):

    contact_at_event_id = models.IntegerField(auto_created=True, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)


