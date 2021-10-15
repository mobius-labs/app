# Generated by Django 3.2.6 on 2021-10-14 09:09

from django.db import migrations


def add_default_sites(apps, schema_editor):
    # We can't import the SocialMediaSite model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    SocialMediaSite = apps.get_model('contact_book', 'SocialMediaSite')

    fb = SocialMediaSite(site='Facebook', url_format='https://www.facebook.com/{username}', icon='facebook-square')
    fb.save()
    instagram = SocialMediaSite(site='Instagram', url_format='https://www.instagram.com/{username}', icon='instagram')
    instagram.save()
    youtube = SocialMediaSite(site='YouTube', url_format='https://www.youtube.com/c/{username}', icon='youtube')
    youtube.save()
    twitter = SocialMediaSite(site='Twitter', url_format='https://twitter.com/{username}', icon='twitter')
    twitter.save()
    linkedin = SocialMediaSite(site='LinkedIn', url_format='https://www.linkedin.com/in/{username}', icon='linkedin')
    linkedin.save()
    github = SocialMediaSite(site='GitHub', url_format='https://github.com/{username}', icon='github')
    github.save()
    github = SocialMediaSite(site='GitHub', url_format='https://github.com/{username}', icon='github')
    github.save()
    other = SocialMediaSite(site='Other', url_format='', icon='')
    other.save()


def remove_default_sites(apps, schema_editor):
    SocialMediaSite = apps.get_model('contact_book', 'SocialMediaSite')
    for site in SocialMediaSite.objects.all():
        site.delete()


def add_default_date_types(apps, schema_editor):
    ImportantDateType = apps.get_model('contact_book', 'ImportantDateType')

    birthday = ImportantDateType(label='Birthday', icon='birthday-cake')
    birthday.save()
    anniversary = ImportantDateType(label='Anniversary', icon='ring')
    anniversary.save()
    other = ImportantDateType(label='Other', icon='calendar-day')
    other.save()


def remove_default_date_types(apps, schema_editor):
    ImportantDateType = apps.get_model('contact_book', 'ImportantDateType')
    for ty in ImportantDateType.objects.all():
        ty.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contact_book', '0004_auto_20211012_0654'),
    ]

    operations = [
        migrations.RunPython(add_default_sites, reverse_code=remove_default_sites),
        migrations.RunPython(add_default_date_types, reverse_code=remove_default_date_types),
    ]
