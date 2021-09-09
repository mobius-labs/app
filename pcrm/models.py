from django.db import models
from enum import Enum


class PronounsChoice(Enum):
    MAL = "he/him"
    FEM = "she/her"
    OTH = "they/them"

# Need to add if null or not null fields


class User(models.Model):
    LoginEmail = models.CharField(max_length=50, primary_key=True)
    DateCreated = models.DateTimeField()
    Password = models.CharField(max_length=45)

    LinkedToContactId = models.OneToOneField('Contact', on_delete=models.CASCADE)


class Contact(models.Model):

    class RegularityOfContact(models.IntegerChoices):
        WK2 = 104
        WK1 = 52
        FRNT = 26
        MNTH = 12
        BIMT = 6
        YR2 = 2
        YR1 = 1

    ContactId = models.IntegerField(auto_created=True, primary_key=True)
    FirstName = models.CharField(max_length=45)
    Surname = models.CharField(max_length=45)
    MiddleName = models.CharField(max_length=45)
    Nickname = models.CharField(max_length=45)
    NamePronunciation = models.CharField(max_length=45)
    Pronouns = models.CharField(
        max_length=15,
        choices=[(tag, tag.value) for tag in PronounsChoice]
    )
    Title = models.CharField(max_length=45),
    Relation = models.CharField(max_length=45),
    Company = models.CharField(max_length=45),
    JobTitle = models.CharField(max_length=45),
    SideNotes = models.TextField(),
    Department = models.CharField(max_length=45),
    RegularityOfContact = models.IntegerField(choices=RegularityOfContact.choices),
    LastTimeContacted = models.DateTimeField()
    LoginOfHostUser = models.ForeignKey(User, on_delete=models.CASCADE)
