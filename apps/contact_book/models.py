from django.db import models
from enum import Enum

from apps.account_page.models import User


class PronounsChoice(Enum):
    MAL = "he/him"
    FEM = "she/her"
    OTH = "they/them"


class ContactMediumLabel(Enum):
    BUS = "business"
    FRN = "friend"
    FAM = "family"
    OTH = "other"


class Contact(models.Model):

    class RegularityOfContact(models.IntegerChoices):
        WK2 = 104
        WK1 = 52
        FRNT = 26
        MNTH = 12
        BIMT = 6
        YR2 = 2
        YR1 = 1

    contact_id = models.IntegerField(auto_created=True, primary_key=True)
    first_name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45, null=True)
    middle_name = models.CharField(max_length=45, null=True)
    nickname = models.CharField(max_length=45, null=True)
    name_pronunciation = models.CharField(max_length=45, null=True)
    pronouns = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in PronounsChoice],
        null=True
    )
    title = models.CharField(max_length=45, null=True),
    relation = models.CharField(max_length=45, null=True),
    company = models.CharField(max_length=45, null=True),
    job_title = models.CharField(max_length=45, null=True),
    side_notes = models.TextField(null=True),
    department = models.CharField(max_length=45, null=True),
    regularity_of_contact = models.IntegerField(choices=RegularityOfContact.choices, null=True),
    last_time_contacted = models.DateTimeField(null=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):

    state = models.CharField(max_length=3, primary_key=True)
    country = models.CharField(max_length=45, primary_key=True)
    postcode = models.CharField(max_length=4, primary_key=True)
    address_line_one = models.CharField(max_length=45, primary_key=True)
    address_line_two = models.CharField(max_length=45, primary_key=True)
    suburb = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    start_of_habitation = models.DateTimeField(null=True)
    end_of_habitation = models.DateTimeField(null=True)
    is_current = models.BooleanField()
    is_hometown = models.BooleanField(null=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)


class Number(models.Model):

    number = models.CharField(max_length=18, primary_key=True)
    label = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in ContactMediumLabel]
    )
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)


class Email(models.Model):

    email_address = models.CharField(max_length=45, primary_key=True)
    label = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in ContactMediumLabel]
    )
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)


class SocialMediaSite(models.Model):

    site = models.CharField(max_length=45, primary_key=True)
    icon = models.CharField(max_length=45, null=True)


class SocialMediaContact(models.Model):

    link = models.CharField(max_length=45, primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    social_media_site = models.ForeignKey(SocialMediaSite, on_delete=models.CASCADE, primary_key=True)


class ImportantDateType(models.Model):

    label = models.CharField(max_length=45, primary_key=True)
    icon = models.CharField(max_length=45, null=True)


class ImportantDate(models.Model):

    important_date_id = models.IntegerField(auto_created=True, primary_key=True)
    date = models.DateTimeField()
    get_alert = models.BooleanField()
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    login_of_host_user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    important_date_type = models.ForeignKey(SocialMediaSite, on_delete=models.CASCADE, primary_key=True)

