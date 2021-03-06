from django.core.validators import RegexValidator
from django.db import models

# from apps.account.models import User
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


# a contact as included in the personal CRM's contact book.
class Contact(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45, null=True, blank=True)
    middle_name = models.CharField(max_length=45, null=True, blank=True)
    nickname = models.CharField(max_length=45, null=True, blank=True)
    name_pronunciation = models.CharField(max_length=45, null=True, blank=True)
    pronouns = models.CharField(max_length=15, choices=PronounsChoice.choices, null=True, blank=True)
    title = models.CharField(max_length=45, null=True, blank=True)
    relation = models.CharField(max_length=45, null=True, blank=True)
    company = models.CharField(max_length=45, null=True, blank=True)
    job_title = models.CharField(max_length=45, null=True, blank=True)
    side_notes = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=45, null=True, blank=True)
    regularity_of_contact = models.IntegerField(choices=RegularityOfContact.choices, null=True, blank=True)
    last_time_contacted = models.DateField(null=True, blank=True)


def save(connected_contact, user):
    user.connected_contact = connected_contact


# each contact has any number of addresses
class Address(models.Model):
    state = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=45, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    address_line_one = models.CharField(max_length=127)
    address_line_two = models.CharField(max_length=127, null=True, blank=True)
    suburb = models.CharField(max_length=45, null=True, blank=True)
    city = models.CharField(max_length=45, null=True, blank=True)
    start_of_habitation = models.DateTimeField(null=True, blank=True)
    end_of_habitation = models.DateTimeField(null=True, blank=True)
    is_current = models.BooleanField(null=True, blank=True)
    is_hometown = models.BooleanField(null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('address_line_one', 'contact')


# each contact has any number of phone numbers
class Number(models.Model):

    number_regex = RegexValidator(regex=r'^\+?1?\d{3,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    number = models.CharField(validators=[number_regex], max_length=15)
    label = models.CharField(max_length=15, choices=ContactMediumLabel.choices, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('number', 'contact')


# each user has any number of emails
class Email(models.Model):

    email_address = models.EmailField(max_length=320)
    label = models.CharField(max_length=15, choices=ContactMediumLabel.choices, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email_address', 'contact')


# models a social media site, either default (added pre-deployment) or a custom one by a user.
class SocialMediaSite(models.Model):

    site = models.CharField(max_length=45, primary_key=True)
    url_format = models.CharField(max_length=255, default="")
    # refers to a particular icon from the FE icon pack, by its name
    icon = models.CharField(max_length=30, default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ['site', 'author']


# each user has any number of social media links
class SocialMediaContact(models.Model):

    link = models.CharField(max_length=300)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    social_media_site = models.ForeignKey(SocialMediaSite, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('link', 'social_media_site', 'contact')


# models a 'type' of important date, ie. a birthday, anniversary, day you met that person
class ImportantDateType(models.Model):

    label = models.CharField(max_length=45, primary_key=True)
    # refers to a particular icon from the FE icon pack, by its name
    icon = models.CharField(max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ['label', 'author']


# each user has any number of important dates associated with it, defined by an important date type.
class ImportantDate(models.Model):

    date = models.DateField()
    get_alert = models.BooleanField(default=False)        # whether the user is alerted on the day
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    important_date_type = models.ForeignKey(ImportantDateType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('contact', 'date', 'important_date_type')
