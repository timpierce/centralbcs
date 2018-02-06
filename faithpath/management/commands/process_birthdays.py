import logging
import importlib

from requests import HTTPError, ConnectionError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from string import Template
from smtplib import SMTPException

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand
from django.conf import settings

from faithpath.models import Child, BirthdayMessage, ActivityLog

record_source = importlib.import_module(settings.RECORD_SOURCE)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Processes birthdays for sending Faith Path emails'

    def handle(self, *args, **options):
        today = datetime.today()
        for child in Child.objects.filter(dob__month=today.month, dob__day=today.day):
            try:
                if child.indvid:
                    person = record_source.get_person(child.indvid)
                else:
                    person = dict(FirstName=child.first_name)

                if person.get('MemberStatus') not in ['Former Member', 'Non-Resident Mem.']:
                    logger.info('Processing birthday for ' + str(child))
                    age = relativedelta(datetime.today(), child.dob).years
                    message = BirthdayMessage.objects.get(pk=age)
                    try:
                        ActivityLog.objects.get(message=message, child=child)
                        logger.warning('Email has been previously sent for ' + str(child))
                    except ActivityLog.MultipleObjectsReturned:
                        logger.warning('Email has been previously sent multiple times for ' + str(child))
                    except ObjectDoesNotExist:

                        # Build Email Address List
                        person['email_to'] = []
                        if child.email_address:
                            person['email_to'].append(child.email_address)
                        for family_member in person.get('FamilyMembers', []):
                            if family_member['FamilyPosition'] in ['Head', 'Spouse']:
                                parent = record_source.get_person(family_member['IndvId'])
                                for email in parent['Emails']:
                                    person['email_to'].append(email['Email'])
                        if age >= settings.FAITH_PATH_MIN_CHILD_EMAIL_AGE:
                            for email in person['Emails']:
                                person['email_to'].append(email['Email'])

                        # Send Email
                        email_addresses = list(set(person['email_to']))
                        logger.info('Email will be sent to ' + str(email_addresses))
                        email = EmailMessage(
                            Template(message.subject).substitute(person),
                            Template(message.content).substitute(person),
                            settings.FAITH_PATH_FROM_EMAIL,
                            email_addresses
                        )
                        email.content_subtype = 'html'
                        if message.attachment:
                            attachment_file = default_storage.open(message.attachment.name, 'rb')
                            attachment_content = attachment_file.read()
                            attachment_file.close()
                            email.attach(message.attachment.name, attachment_content, 'application/pdf')
                        email.send()

                        # Log that the email was sent
                        ActivityLog(child=child, message=message).save()
            except SMTPException, e:
                logger.error('Cannot process {}. {}'.format(child, e.message))
            except KeyError, e:
                logger.error('Cannot process {}. The field {} does not exist.'.format(child, e.message))
            except ObjectDoesNotExist:
                logger.info(
                    'There is no message established for {} year olds. Skipping id: {}'.format(age, child))
            except ConnectionError, e:
                logger.info(e)
            except HTTPError, e:
                if e.response.status_code == 404:
                    logger.warning('The record for {} no longer exists in ACS.'.format(child))
        self.stdout.write(self.style.SUCCESS('Successfully processed birthdays'))
