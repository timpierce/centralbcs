import os


SERVER_EMAIL = 'timpierce.py@gmail.com'
SITE_ID = 1
SITE_HEADER = 'Central Baptist Church'
SITE_TITLE = 'Central Baptist Church'

################
# ACS Settings #
################
ACS_SITE_ID = 11607
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