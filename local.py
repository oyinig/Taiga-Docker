# Please modify this file as needed, see the local.py.example for details:
# https://github.com/taigaio/taiga-back/blob/master/settings/local.py.example

from .common import *
from .original import *
import os, sys
import pem
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="error.log", level=logging.INFO)

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') # You cannot use both (TLS and SSL) at the same time!
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

IMPORTERS["jira"]["active"] = os.getenv('JIRA_IMPORTER_ACTIVE')
IMPORTERS["jira"]["consumer_key"] = os.getenv('JIRA_IMPORTER_CONSUMER_KEY')
pub_cert = pem.parse_file("../public_key.pem")
cert =  pem.parse_file("../private_key.pem")

logger.info("---Certificate logging---")
IMPORTERS["jira"]["cert"] = open("../private_key.pem", "r").read()
IMPORTERS["jira"]["pub_cert"] = open("../private_key.pem", "r").read()
logger.info("The value of var from pem lib (public) is %s", pub_cert[0])
logger.info("The value of var from pem lib (private) is %s", cert[0])
logger.info("The value of var from pem lib (public) is %s", IMPORTERS["jira"]["cert"])
logger.info("The value of var from pem lib (private) is %s", IMPORTERS["jira"]["pub_cert"])
    
 

IMPORTERS["github"]["active"] = os.getenv('GITHUB_ACTIVE')
IMPORTERS["github"]["client_id"] = os.getenv('GITHUB_CLIENT_ID')
IMPORTERS["github"]["client_secret"] = os.getenv('GIITHUB_CLIENT_SECRET')
 
 
IMPORTERS["trello"]["active"] = os.getenv('TRELLO_ACTIVE')
IMPORTERS["trello"]["api_key"] = os.getenv('TRELLO_API_KEY')
IMPORTERS["trello"]["secret_key"] = os.getenv('TRELLO_SECRET_KEY')


IMPORTERS["asana"]["active"] = os.getenv('ASANA_ACTIVE')
IMPORTERS["asana"]["callback_url"] = os.getenv('ASANA_CALLBACK_URL')
IMPORTERS["asana"]["app_id"] = os.getenv('ASANA_APP_ID')
IMPORTERS["asana"]["app_secret"] = os.getenv('ASANA_APP_SECERET')
 





# Set configured database parameters
DATABASES['default']['NAME'] = os.getenv('TAIGA_DB_NAME')
DATABASES['default']['HOST'] = os.getenv('POSTGRES_PORT_5432_TCP_ADDR') or os.getenv('TAIGA_DB_HOST')
DATABASES['default']['USER'] = os.getenv('TAIGA_DB_USER')
DATABASES['default']['PASSWORD'] = os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD') or os.getenv('TAIGA_DB_PASSWORD')
DATABASES['default']['PORT'] = 5432

# Configure hostname and URLs
SITES['api']['domain'] = os.getenv('TAIGA_HOSTNAME')
SITES['front']['domain'] = os.getenv('TAIGA_HOSTNAME')
MEDIA_URL  = 'http://' + os.getenv('TAIGA_HOSTNAME') + '/media/'
STATIC_URL = 'http://' + os.getenv('TAIGA_HOSTNAME') + '/static/'

# If running on SSL externally, change scheme and URLs accordingly
if os.getenv('TAIGA_SSL').lower() == 'true':
    SITES['api']['scheme'] = 'https'
    SITES['front']['scheme'] = 'https'
    MEDIA_URL  = 'https://' + os.getenv('TAIGA_HOSTNAME') + '/media/'
    STATIC_URL = 'https://' + os.getenv('TAIGA_HOSTNAME') + '/static/'

SECRET_KEY = os.getenv('TAIGA_SECRET_KEY')

# Enable or disable public registration
PUBLIC_REGISTER_ENABLED = (os.getenv('TAIGA_PUBLIC_REGISTER_ENABLED').lower() == 'true')

# Enable or disable debugging
DEBUG = (os.getenv('TAIGA_BACKEND_DEBUG').lower() == 'true')
TEMPLATE_DEBUG = (os.getenv('TAIGA_BACKEND_DEBUG').lower() == 'true')

# Configure LDAP backend (if enabled)
if os.getenv('LDAP_ENABLE').lower() == 'true':
    INSTALLED_APPS += ["taiga_contrib_ldap_auth"]
    LDAP_SERVER = os.getenv('LDAP_SERVER')
    LDAP_PORT = int(os.getenv('LDAP_PORT'))
    # Full DN of the service account use to connect to LDAP server and search for login user's account entry
    # If LDAP_BIND_DN is not specified, or is blank, then an anonymous bind is attempated
    LDAP_BIND_DN = os.getenv('LDAP_BIND_DN')
    LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD')
    # Starting point within LDAP structure to search for login user
    LDAP_SEARCH_BASE = os.getenv('LDAP_SEARCH_BASE')
    # LDAP property used for searching, ie. login username needs to match value in sAMAccountName property in LDAP
    LDAP_SEARCH_PROPERTY = os.getenv('LDAP_SEARCH_PROPERTY')
    LDAP_SEARCH_SUFFIX = None
    # Names of LDAP properties on user account to get email and full name
    LDAP_EMAIL_PROPERTY = os.getenv('LDAP_EMAIL_PROPERTY')
    LDAP_FULL_NAME_PROPERTY = os.getenv('LDAP_FULL_NAME_PROPERTY')
