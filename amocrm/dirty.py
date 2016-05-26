import amocrm.conf
from amocrm.manager import Manager
from amocrm.models.field import (
    Field, 
    PhoneField,
    EmailField,
    NoteField,
    UrlField,
)
from amocrm.models.value import Value
from amocrm.models.entities.lead import Lead
from amocrm.models.entities.contact import Contact

# user
AMO_USER_URL   = "https://smileenglish.amocrm.ru"
AMO_USER_LOGIN = "order@smileenglish.ru"
AMO_USER_HASH  = "ff7286ac1f1a65838a253589380ac2f4"

am = Manager()

amo_settings = amocrm.conf.settings
# amo_settings['AMO_USER_LOGIN'] = AMO_USER_LOGIN
amo_settings.USER_LOGIN  = AMO_USER_LOGIN
amo_settings.USER_HASH   = AMO_USER_HASH
amo_settings.USER_DOMAIN = AMO_USER_URL

amo_settings.PHONE_ID = 414772
amo_settings.EMAIL_ID = 414774
amo_settings.URL_ID   = 443656
amo_settings.NOTE_ID  = 457172

amo_settings.PHONE_DEFAULT_ENUM = 'HOME'
amo_settings.EMAIL_DEFAULT_ENUM = '976706'
amo_settings.NOTE_DEFAULT_ENUM  = None
amo_settings.URL_DEFAULT_ENUM   = None

# amo_settings.PIPELINE_BETA = 172563
PIPELINE_CLIENTS  =  9211617
PIPELINE_TEACHERS = 10886418
PIPELINE_SCHOOLS  = 10958649
PIPELINE_BETA     = 10996971



# phone_value = Value(value='322 223 322', enum='HOME')
# email_value = Value(value='sashoo@sashoo.org')
# url_value = Value(value='/kids/')
# note_value = Value(value='Заявка методисту')

# phone_field = PhoneField(values=phone_value)
# email_field = EmailField(values=email_value)
# url_field   = UrlField(values=url_value)
# note_field  = NoteField(values=note_value)
     
name = 'Контакт из API, не обращать внимание'
tags = 'beta'
# fields = [
#     phone_field='555 555 555',
#     email_field='mail@example.org',
#     url_field='/thanks/',
#     note_field='Заявка методисту',
# ]

fields = [
    PhoneField(values='555 555 555'),
    EmailField(values='mail@example.org'),
    UrlField(values='/thanks/'),
    NoteField(values='Заявка методисту'),
]

r_auth = am.auth()

lead = Lead(
    name='beta lead from API',
    status_id=PIPELINE_BETA
)
response_lead = am.post_entity(lead)


contact = Contact(
    name=name, 
    fields=fields,
    tags='Заявка,beta',
    linked_leads=lead,
)
# response_contact = am.post_entity(contact)


# # # a = am.get_account_info()
# # # c = am.get_contacts()
# # # l = am.get_leads()

import pdb
pdb.set_trace()


