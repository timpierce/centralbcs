import itertools
import logging
import importlib
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from requests import HTTPError

from faithpath.models import Child

record_source = importlib.import_module(settings.RECORD_SOURCE)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports children from ChMS system'

    def handle(self, *args, **options):
        """
        Imports children from the ACS system. It looks for the most recent ID in the database and counts up from there. If
        there are fifty 404s in a row it stops its loop.
        """
        last_id = 0
        try:
            last_id = Child.objects.order_by('indvid').last().indvid
            logger.info("Last ID found in the database is: {}".format(last_id))
        except AttributeError:
            logger.warning('There are no members in database.')

        count_404 = 0
        for i in itertools.count(start=last_id + 1):
            logger.info('Processing for import id: {}'.format(i))
            try:
                person = record_source.get_person(i)
                count_404 = 0  # Reset 404 counter. If we find a record we try for ACS_MAX_HTTP_404 more people.
                logger.info(person)
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
                    logger.warning(e)
            except Exception, e:
                logger.warning(e)
        self.stdout.write(self.style.SUCCESS('Successfully imported children'))
