import os


SERVER_EMAIL = 'timpierce.py@gmail.com'
EMAIL_BACKEND = 'django_ses.SESBackend'

################
# AWS SETTINGS #
################
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'centralbcs'

################
# ACS Settings #
################
ACS_SEC_ID = os.getenv('ACS_SEC_ID')
ACS_SITE_ID = 11607
ACS_SOAP_URL = 'https://secure.accessacs.com/acscfwsv2/wsca.asmx'
ACS_SOAP_IMPORT_FILTER = 'http://acstechnologies.com/'
ACS_USER = os.getenv('ACS_USER')
ACS_PASS = os.getenv('ACS_PASS')

#######################
# Faith Path Settings #
#######################
FAITH_PATH_FROM_EMAIL = 'faithpath@centralbcs.org'
FAITH_PATH_MIN_CHILD_EMAIL_AGE = 16

###############################
# Face 2 Face Signup Settings #
###############################
# Email addresses to send a notification to once the GROUP_SIGNUP_ACTIVE flag is False.
F2F_FROM_EMAIL = 'smallgroups@centralbcs.org'

# Export Fields
EXPORT_FIELDS = ['id', 'group', 'ministry', 'student_class', 'first_name', 'last_name', 'gender', 'dob',
                 'phone', 'email', 'address', 'address2', 'city', 'state', 'postal_code', 'comments']