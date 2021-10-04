from django.db import models
from enum import Enum

from apps.account.models import User
from backend_crm import settings


class PronounsChoice(models.TextChoices):
    MAL = "he/him"
    FEM = "she/her"
    OTH = "they/them"


class ContactMediumLabel(models.TextChoices):
    BUS = "business"
    FRN = "friend"
    FAM = "family"
    OTH = "other"


class RegularityOfContact(models.IntegerChoices):
    WK2 = 104
    WK1 = 52
    FRNT = 26
    MNTH = 12
    BIMT = 6
    YR2 = 2
    YR1 = 1


class Contact(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45, null=True)
    middle_name = models.CharField(max_length=45, null=True)
    nickname = models.CharField(max_length=45, null=True)
    name_pronunciation = models.CharField(max_length=45, null=True)
    pronouns = models.CharField(max_length=15, choices=PronounsChoice.choices, null=True)
    title = models.CharField(max_length=45, null=True)
    relation = models.CharField(max_length=45, null=True)
    company = models.CharField(max_length=45, null=True)
    job_title = models.CharField(max_length=45, null=True)
    side_notes = models.TextField(null=True)
    department = models.CharField(max_length=45, null=True)
    regularity_of_contact = models.IntegerField(choices=RegularityOfContact.choices, null=True)
    last_time_contacted = models.DateTimeField(null=True)


class Address(models.Model):
    state = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=45, null=True)
    postcode = models.CharField(max_length=10, null=True)
    address_line_one = models.CharField(max_length=45)
    address_line_two = models.CharField(max_length=45, null=True)
    suburb = models.CharField(max_length=45, null=True)
    city = models.CharField(max_length=45, null=True)
    start_of_habitation = models.DateTimeField(null=True)
    end_of_habitation = models.DateTimeField(null=True)
    is_current = models.BooleanField()
    is_hometown = models.BooleanField(null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('address_line_one', 'contact')


class Number(models.Model):
    number = models.CharField(max_length=18)
    label = models.CharField(max_length=15, choices=ContactMediumLabel.choices, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('number', 'contact')


class Email(models.Model):

    email_address = models.CharField(max_length=45)
    label = models.CharField(max_length=15, choices=ContactMediumLabel.choices, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email_address', 'contact')


class SocialMediaSite(models.Model):

    site = models.CharField(max_length=45, primary_key=True)
    icon = models.ImageField(null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ['site', 'is_default']


class SocialMediaContact(models.Model):

    link = models.CharField(max_length=45)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    social_media_site = models.ForeignKey(SocialMediaSite, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('link', 'social_media_site', 'contact')


class ImportantDateType(models.Model):

    label = models.CharField(max_length=45, primary_key=True)
    icon = models.ImageField(null=True)
    is_default = models.BooleanField()

    class Meta:
        unique_together = ['label', 'is_default']


class ImportantDate(models.Model):

    date = models.DateField()
    get_alert = models.BooleanField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    important_date_type = models.ForeignKey(ImportantDateType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('contact', 'date', 'important_date_type')
