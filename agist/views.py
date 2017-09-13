# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
import logging
from datetime import datetime
from string import Template

import requests
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.mail.message import EmailMessage
from django.http import HttpResponse
from requests import HTTPError

from models import Child, BirthdayMessage

logging.basicConfig(level=logging.INFO)


def get_person(indvid, retry=5):
    for i in range(retry):
        try:
            r = requests.get(
                'https://secure.accessacs.com/api_accessacs_mobile/v2/{}/individuals/{}'.format(settings.ACS_SITE_ID, indvid),
                auth=(settings.ACS_USER, settings.ACS_PASS)
            )
            r.raise_for_status()
            return r.json()
        except requests.ConnectionError, e:
            logging.info(e)
    raise requests.ConnectionError("Max connection retries for get_person exceeded. Cannot connect to ACS for id: " + indvid)


def import_children(request):
    """
    Imports children from the ACS system. It looks for the most recent ID in the database and counts up from there. If
    there are fifty 404s in a row it stops its loop.
    """
    last_id = 0
    try:
        last_id = Child.objects.order_by('indvid').last().indvid
        logging.info("AGIST: Last ID found in the database is: {}".format(last_id))
    except AttributeError:
        logging.info('There are no members in database.')

    count_404 = 0
    for i in itertools.count(start=last_id + 1):
        logging.info('Processing for import id: {}'.format(i))
        try:
            person = get_person(i)
            count_404 = 0  # Reset 404 counter. If we find a record we try for ACS_MAX_HTTP_404 more people.
            logging.info(person)
            if person['DateOfBirth']:
                dob = datetime.strptime(person['DateOfBirth'], '%m/%d/%Y')
                if relativedelta(datetime.today(), dob).years < 18:
                    child = Child()
                    child.indvid = i
                    child.dob = dob
                    child.save()
        except HTTPError, e:
            if e.response.status_code == 404:
                count_404 += 1
                if count_404 >= 50:
                    break
            else:
                logging.warning(e)
        except Exception, e:
            logging.warning(e)
    return HttpResponse(status=200)


def process_birthdays(request):
    # Get list of birthdays
    birthdays = []
    today = datetime.today()
    for child in Child.objects.filter(dob__month=today.month, dob__day=today.day):
        person = get_person(child.indvid)
        if person['MemberStatus'] not in ['Former Member', 'Non-Resident Mem.']:
            birthdays.append(person)
    logging.info('Found {} birthdays for today.'.format(len(birthdays)))

    for child in birthdays:
        try:
            logging.info('Processing birthday for ' + str(child['IndvId']))
            age = relativedelta(datetime.today(), datetime.strptime(child['DateOfBirth'], '%m/%d/%Y')).years
            message = BirthdayMessage.objects.get(pk=age)
            # Build Email Address List
            child['email_to'] = []
            for family_member in child['FamilyMembers']:
                if family_member['FamilyPosition'] in ['Head', 'Spouse']:
                    parent = get_person(family_member['IndvId'])
                    for email in parent['Emails']:
                        child['email_to'].append(email['Email'])

            if age >= settings.AGIST_MIN_CHILD_EMAIL_AGE:
                for email in child['Emails']:
                    child['email_to'].append(email['Email'])

            # Send Email
            email_addresses = list(set(child['email_to']))
            logging.info('Email will be sent to ' + str(email_addresses))
            email = EmailMessage(
                Template(message.subject).substitute(child),
                Template(message.content).substitute(child),
                settings.AGIST_FROM_EMAIL,
                # TODO: Use actual email addresses
                # email_addresses,
                ['tim@pierce-fam.com']
            )
            email.content_subtype = 'html'
            if message.attachment:
                attachment_file = default_storage.open(message.attachment.name, 'rb')
                attachment_content = attachment_file.read()
                attachment_file.close()
                email.attach(message.attachment.name, attachment_content, 'application/pdf')
            email.send()
            # TODO: throwing a TypeError when there is an incorrect key in template.
        except ObjectDoesNotExist:
            logging.info(
                'Agist: There is no message established for {} year olds. Skipping id: {}'.format(age, child['IndvId']))
        except requests.ConnectionError, e:
            logging.info(e)
    return HttpResponse(status=200)
