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


# models an event to be included on the calendar
class Event(models.Model):

    title = models.CharField(max_length=45)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=45, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    tag = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in EventTag],
        null=True,
        blank=True
    )
    response = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in EventResponse],
        null=True,
        blank=True
    )
    is_public = models.BooleanField(default=True)
    alert = models.DateTimeField(null=True, blank=True)


# each event occurs any number of times.
class EventOccurrence(models.Model):

    date = models.DateTimeField()
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


# to be properly modelled in the third sprint
'''
class EventIncludesContact(models.Model):

    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
'''

