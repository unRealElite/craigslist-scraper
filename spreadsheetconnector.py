import gdata.docs.service
import atom.core
from spreadsheet_config import settings

POST_TEMPLATE = '{}%s'

client = gdata.docs.service.DocsService()
client.ClientLogin(settings.username, settings.password)

documents_feed = client.GetDocumentListFeed()
for e in documents_feed.entry:
    print e.title.text


#
client.Post()


#classes must match header titles
class Apartment(atom.core.XmlElement):
    hook = 'hook'
    price = 'price'
    link = 'link'


class ApartmentEntry(gdata.data.GDEntry):
	_qname = atom.data.ATOM_TEMPLATE % 'entry'
	apartment = [Apartment]


class ApartmentFeed(gdata.data.GDFeed):
	_qname = atom.data.ATOM_TEMPLATE % 'feed'
	entry = [ApartmentEntry]