import os

SERVER_EMAIL = 'timpierce.py@gmail.com'
EMAIL_BACKEND = 'django_ses.SESBackend'

################
# AWS SETTINGS #
################
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'centralbcs'
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')


################
# ACS Settings #
################
ACS_SITE_ID = 11607
ACS_USER = os.environ.get('ACS_USER')
ACS_PASS = os.environ.get('ACS_PASS')


#######################
# Faith Path Settings #
#######################
AGIST_FROM_EMAIL = 'faithpath@centralbcs.org'
AGIST_MIN_CHILD_EMAIL_AGE = 16

###############################
# Face 2 Face Signup Settings #
###############################
# Number of total members that can automatically sign up for a group before it closes.
NUMBER_OF_MEMBERS = {'adult_education': 16, 'college': 10}

# Email addresses to send a notification to once the GROUP_SIGNUP_ACTIVE flag is False.
STAFF_NOTIFICATION_EMAIL = 'smallgroups@centralbcs.org'

# Export Fields
EXPORT_FIELDS = ['id','group', 'ministry', 'student_class', 'first_name', 'last_name', 'gender', 'dob',
                 'phone', 'email', 'address', 'address2', 'city', 'state', 'postal_code', 'comments']
