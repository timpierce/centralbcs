import logging

from django.conf import settings
from zeep import Client


logging.basicConfig(level=logging.INFO)
client = Client(settings.ACS_URL + '?WSDL')
login_token = client.service.getLoginToken(siteid=settings.ACS_SITE_ID, secid=settings.ACS_SEC_ID)

# Master Group
# 1744 - Face to Face Groups

"""

1744 - Face to Face Groups (getMasterClassesl3)

Group Positions (clsGetPositions)
1624 Member
1625 Prospect
1626 Leader
1627 Host
3754 College Student
3755 College Connect Ldr


"""

'''
for i in range(last_id + 1, last_id + 50000):
    try:
        response = client.service.getPersonbyID(token=login_token, personid=i)
        person = response['_value_1'].getiterator('dbs')[0]
        try:
            dob = parse_date(person.find('DOB').text[:10])
            if relativedelta(datetime.today(), dob).years < 18:
                member = Member()
                member.indv_id = person.find('IndvID').text
                member.family_id = person.find('PrimFamily').text
                member.dob = dob
                member.save()
        except AttributeError:
            logging.warning('Attribute Error for {}'.format(i))
    except AttributeError, e:
        logging.info('Person not found for id {}'.format(i))
    except ValueError, e:
        logging.error('AGIST VALUE ERROR: {}'.format(e.message))
'''
"""
for member in Member.objects.all():
    try:
        action = Action.objects.get(age=member.get_age())
        if action and not ActionLog.objects.get(indv_id=member.indv_id, action=action):
            # TODO: get family id
            # TODO: get parents id
            # TODO: get parents email
            # TODO: perform action
            # TODO: Log action
            logging.info('AGIST: Performing action {}'.format(action.id))
    except Action.DoesNotExist:
        continue
"""
