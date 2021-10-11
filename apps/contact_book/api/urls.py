from django.urls import path

from apps.contact_book.api.views import (
    create_contact, get_contact_by_id, get_all_contacts, delete_contact_by_id, update_contact_by_id,
    create_phone_no, get_phone_nos_by_cid, delete_phone_no_by_pid, update_phone_no_by_pid,
    create_address, get_addresses_by_cid, delete_address_by_aid, update_address_by_aid,
    create_email, get_emails_by_cid, delete_email_by_eid, update_email_by_eid, create_social_media_site,
    get_social_media_sites, create_social_media_contact, get_socials_by_cid, delete_social_by_sid,
    update_social_media_contact, get_important_date_types, create_important_date_type, create_important_date,
    get_important_dates, delete_important_date, update_important_date
)

app_name = 'contact_book'

urlpatterns = [
    # contacts
    path('create_contact', create_contact, name="create_contact"),
    path('get_contact_by_id/<int:contact_id>', get_contact_by_id, name="get_contact_by_id"),
    path('get_all_contacts', get_all_contacts, name="get_all_contacts"),
    path('delete_contact_by_id/<int:contact_id>', delete_contact_by_id, name="delete_contact_by_id"),
    path('update_contact_by_id/<int:contact_id>', update_contact_by_id, name="update_contact_by_id"),

    # phone numbers
    path('create_phone_no/<int:contact_id>', create_phone_no, name="create_phone_no"),
    path('get_phone_nos_by_cid/<int:contact_id>', get_phone_nos_by_cid, name="get_phones_no_by_cid"),
    path('delete_phone_no_by_pid/<int:number_id>', delete_phone_no_by_pid, name="delete_phone_no_by_pid"),
    path('update_phone_no_by_pid/<int:number_id>', update_phone_no_by_pid, name="update_phone_no_by_pid"),

    # addresses
    path('create_address/<int:contact_id>', create_address, name="create_address"),
    path('get_addresss_by_cid/<int:contact_id>', get_addresses_by_cid, name="get_addresses_by_cid"),
    path('delete_address_by_aid/<int:address_id>', delete_address_by_aid, name="delete_address_by_aid"),
    path('update_address_by_aid/<int:address_id>', update_address_by_aid, name="update_address_by_aid"),

    # emails
    path('create_email/<int:contact_id>', create_email, name="create_email"),
    path('get_emails_by_cid/<int:contact_id>', get_emails_by_cid, name="get_emails_by_cid"),
    path('delete_email_by_eid/<int:email_id>', delete_email_by_eid, name="delete_email_by_eid"),
    path('update_email_by_eid/<int:email_id>', update_email_by_eid, name="update_email_by_eid"),

    # social media sites
    path('create_social_media_site/', create_social_media_site, name="create_social_media_site"),
    path('get_social_media_sites/', get_social_media_sites, name="get_social_media_sites"),
    path('create_social_media_contact/<int:contact_id>', create_social_media_contact,
         name="create_social_media_contact"),
    path('get_social_media_contacts_by_cid/<int:contact_id>', get_socials_by_cid, name="get_socials_by_cid"),
    path('delete_social_media_contact_by_sid/<int:social_media_contact_id>', delete_social_by_sid,
         name="delete_social_by_sid"),
    path('update_social_media_contact_by_sid/<int:social_media_contact_id>', update_social_media_contact,
         name="update_social_media_contact"),

    # important dates
    path('create_important_date_type/', create_important_date_type, name='create_important_date_type'),
    path('get_important_date_types/', get_important_date_types, name='get_important_date_types'),
    path('create_important_date/<int:contact_id>', create_important_date, name='create_important_date'),
    path('get_important_dates_by_cid/<int:contact_id>', get_important_dates, name='get_important_dates'),
    path('delete_important_date_by_iid/<int:important_date_id>', delete_important_date, name='delete_important_date'),
    path('update_important_date_by_iid/<int:important_date_id>', update_important_date, name='update_important_date'),


]