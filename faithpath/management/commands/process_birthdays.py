import logging

from requests import HTTPError, ConnectionError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from string import Template


from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand
from django.conf import settings

from faithpath.models import Child, BirthdayMessage, ActivityLog
from faithpath.management.acs import get_person


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Processes birthdays for sending Faith Path emails'

    def handle(self, *args, **options):
        today = datetime.today()
        for child in Child.objects.filter(dob__month=today.month, dob__day=today.day):
            try:
                person = get_person(child.indvid)
                if person['MemberStatus'] not in ['Former Member', 'Non-Resident Mem.']:
                    logger.info('Processing birthday for ' + str(child.indvid))
                    age = relativedelta(datetime.today(), child.dob).years
                    message = BirthdayMessage.objects.get(pk=age)
                    try:
                        ActivityLog.objects.get(message=message, child=child.indvid)
                        logger.warning('Email has been previously sent for ' + str(child.indvid))
                    except ActivityLog.MultipleObjectsReturned:
                        logger.warning('Email has been previously sent multiple times for ' + str(child.indvid))
                    except ObjectDoesNotExist:

                        # Build Email Address List
                        person['email_to'] = []
                        for family_member in person['FamilyMembers']:
                            if family_member['FamilyPosition'] in ['Head', 'Spouse']:
                                parent = get_person(family_member['IndvId'])
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

                        # Log that the email was sent
                        activity_log = ActivityLog()
                        activity_log.child = child
                        activity_log.message = message
                        activity_log.save()
            except KeyError, e:
                logger.error('Cannot process {}. The field {} does not exist.'.format(child.indvid, e.message))
            except ObjectDoesNotExist:
                logger.info(
                    'There is no message established for {} year olds. Skipping id: {}'.format(age, child.indvid))
            except ConnectionError, e:
                logger.info(e)
            except HTTPError, e:
                if e.response.status_code == 404:
                    logger.warning('The record for {} no longer exists in ACS.'.format(child.indvid))
        self.stdout.write(self.style.SUCCESS('Successfully processed birthdays'))
