from django.contrib import admin
from apps.contact_book.models import *
# Register your models here.

admin.site.register(Contact)
admin.site.register(Number)
admin.site.register(Address)
admin.site.register(Email)
admin.site.register(SocialMediaSite)
admin.site.register(SocialMediaContact)
admin.site.register(ImportantDateType)
admin.site.register(ImportantDate)