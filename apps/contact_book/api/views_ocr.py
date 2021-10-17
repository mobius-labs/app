import os

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.contact_book.api.forms import BusinessCardOcrForm
from apps.contact_book.api.serializers import FullContactSerializer
from apps.contact_book.models import *


def try_save_model(m, messages):
    try:
        m.save()
    except Exception as e:
        msg = 'unknown'
        if e.args and e.args[0]:
            msg = e.args[0]
        message = f'failed to save {m}, reason: {msg}'
        messages.append(message)
        print(f'Warning: {message}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def business_card_ocr(request):
    # This view was inspired by the example from the Azure SDK
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/samples/v3.2-beta/sample_analyze_business_cards.py

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import FormRecognizerClient

    ENDPOINT = 'AZURE_FORM_RECOGNIZER_ENDPOINT'
    KEY = 'AZURE_FORM_RECOGNIZER_KEY'

    if KEY not in os.environ or ENDPOINT not in ENDPOINT:
        return Response({'messages': ['Missing Azure API Key']}, status=400)

    endpoint = os.environ[ENDPOINT]
    key = os.environ[KEY]

    form = BusinessCardOcrForm(request.POST, request.FILES)
    if not form.is_valid():
        return Response({'errors': form.errors}, status=400)

    image = request.FILES['image']

    messages = []

    client = FormRecognizerClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    image_contents = image.read()

    poller = client.begin_recognize_business_cards(business_card=image_contents, locale="en-AU")
    business_cards = poller.result()

    for idx, business_card in enumerate(business_cards):
        print("--------Recognizing business card #{}--------".format(idx + 1))

        raw_result = business_card.to_dict()

        contact = Contact(author=request.user)

        contact_names = business_card.fields.get("ContactNames")
        if contact_names and len(contact_names.value) > 0:
            name = contact_names.value[0]
            if "FirstName" in name.value:
                contact.first_name = name.value["FirstName"].value
            if "LastName" in name.value:
                contact.surname = name.value["LastName"].value

            # swap them if needed
            if not contact.first_name and contact.surname:
                contact.first_name = contact.surname
                contact.surname = ""
        company_names = business_card.fields.get("CompanyNames")
        if company_names and len(company_names.value) > 0:
            contact.company = company_names.value[0].value
        departments = business_card.fields.get("Departments")
        if departments and len(departments.value) > 0:
            contact.department = departments.value[0].value
        job_titles = business_card.fields.get("JobTitles")
        if job_titles and len(job_titles.value) > 0:
            contact.job_title = job_titles.value[0].value

        contact.save()
        messages.append(f'Contact saved with id #{contact.id}')

        emails = business_card.fields.get("Emails")
        if emails:
            for email in emails.value:
                try_save_model(Email(contact=contact, email_address=email.value, label='other'), messages)

        websites = business_card.fields.get("Websites")
        if websites:
            for website in websites.value:
                try_save_model(SocialMediaContact(contact=contact, link=website.value, social_media_site=SocialMediaSite.objects.get(site='Other')), messages)

        addresses = business_card.fields.get("Addresses")
        if addresses:
            for address in addresses.value:
                try_save_model(Address(contact=contact,address_line_one=address.value, is_current=True), messages)

        mobile_phones = business_card.fields.get("MobilePhones")
        if mobile_phones:
            for phone in mobile_phones.value:
                try_save_model(Number(contact=contact, number=phone.value), messages)

        faxes = business_card.fields.get("Faxes")
        if faxes:
            for fax in faxes.value:
                try_save_model(Number(contact=contact, number=fax.value, label='business'), messages)

        work_phones = business_card.fields.get("WorkPhones")
        if work_phones:
            for work_phone in work_phones.value:
                try_save_model(Number(contact=contact, number=work_phone.value, label='business'), messages)

        other_phones = business_card.fields.get("OtherPhones")
        if other_phones:
            for other_phone in other_phones.value:
                try_save_model(Number(contact=contact, number=other_phone.value_data.text, label='other'), messages)

        return Response({
            'item': FullContactSerializer(contact).data,
            'messages': messages,
            'raw_result': raw_result
        })

    return Response({'messages': ['No business card detected']}, status=400)



