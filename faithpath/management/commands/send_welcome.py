import logging
import importlib
from smtplib import SMTPRecipientsRefused
from string import Template

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand
from requests import HTTPError, ConnectionError

from faithpath.models import Child, BirthdayMessage, ActivityLog

record_source = importlib.import_module(settings.RECORD_SOURCE)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends welcome to FaithPATH emails'

    def handle(self, *args, **options):
        for child in Child.objects.filter(pk__gte=3929):
            try:
                if child.indvid:
                    person = record_source.get_person(child.indvid)
                else:
                    person = dict(FirstName=child.first_name)

                if person.get('MemberStatus') not in ['Former Member', 'Non-Resident Mem.']:
                    logger.info('Processing welcome emails for ' + str(child))
                    message = BirthdayMessage.objects.get(pk=100)
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

                        # Send Email
                        email_addresses = list(set(person['email_to']))
                        logger.info('Email will be sent to ' + str(email_addresses))
                        email = EmailMessage(
                            Template(message.subject).substitute(person),
                            Template(message.content).substitute(person),
                            settings.FAITH_PATH_FROM_EMAIL,
                            email_addresses,
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
            except SMTPRecipientsRefused, e:
                logger.error('Cannot process {}. {}.'.format(child, e.message))
            except KeyError, e:
                logger.error('Cannot process {}. The field {} does not exist.'.format(child, e.message))
            except ConnectionError, e:
                logger.info(e)
            except HTTPError, e:
                if e.response.status_code == 404:
                    logger.warning('The record for {} no longer exists in ACS.'.format(child))
        self.stdout.write(self.style.SUCCESS('Successfully processed welcome emails.'))
