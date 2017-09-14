import os

####################
# AWS SES SETTINGS #
####################
SERVER_EMAIL = 'timpierce.py@gmail.com'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'


###################
# AWS S3 Settings #
###################
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAIPY4ELE2HH5JETWA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'centralbcs'


################
# ACS Settings #
################
ACS_SEC_ID = "$3cY%8xbno?baMvpXX_XQ?QZ1C"
ACS_SITE_ID = 11607
ACS_SOAP_URL = 'https://secure.accessacs.com/acscfwsv2/wsca.asmx'
ACS_SOAP_IMPORT_FILTER = 'http://acstechnologies.com/'
ACS_USER = 'jpierce'
ACS_PASS = 'mshmother3'


##################
# Agist Settings #
##################
AGIST_FROM_EMAIL = 'faithpath@centralbcs.org'
AGIST_MIN_CHILD_EMAIL_AGE = 16

###############################
# Face 2 Face Signup Settings #
###############################
# Number of total members that can automatically sign up for a group before it closes.
NUMBER_OF_MEMBERS = {'adult_education': 16, 'college': 10}

# Email addresses to send a notification to once the GROUP_SIGNUP_ACTIVE flag is False.
STAFF_NOTIFICATION_EMAIL = 'smallgroups@centralbcs.org'

# Whether the list display is available to choose a group to join. If True then the list is available and user can
# choose their own group. If False then the list is not available and user will be presented with a form that they can
# fill in. Staff will find a group for them out of band and the notification email will be sent to the staff, however a
# notification email will not be sent to the user.
GROUP_SIGNUP_ACTIVE = True

# Export Fields
EXPORT_FIELDS = ['id','group', 'ministry', 'student_class', 'first_name', 'last_name', 'gender', 'dob',
                 'phone', 'email', 'address', 'address2', 'city', 'state', 'postal_code', 'comments']
