import requests
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


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
            logger.info(e)
    raise requests.ConnectionError("Max connection retries for get_person exceeded. Cannot connect to ACS for id: " + indvid)