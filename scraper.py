#!/usr/bin/env python
# Copyright 2011 Ankur Goyal
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import BeautifulSoup
from termcolor import cprint
import md5
import re
import time
import urllib2
from mailer import Mailer
from mailer import Message
from config import settings

RECPIPENTS = ['example@server1.com', 'example@server2.com', 'example@server3.com']

PRICE_REGEX = re.compile('\$([\d]+)')
BEDROOM_REGEX = re.compile('/\d[b][r]/gi')
all_entries = {}


def parse_entry(entry):
    ret = {}

    #Unique ID
    ret['id'] = md5.md5(str(entry)).hexdigest()

    #Link to the listing
    link = entry.find('span', {'class': 'pl'}).find('a')
    ret['link'] = link['href']

    #Link content
    hook = link.contents[0]
    ret['hook'] = hook

    #Bedrooms
    beds = entry.find('span', {'class':'12'})
    parseBeds = BEDROOM_REGEX.search(beds)
    bed_match = False
    if parseBeds:
        ret['beds'] = str(parseBeds.group(1))
        print ret['beds']
        if ret['beds'] == settings.bedrooms:
            bed_match = True

    #Price
    price = entry.find('span', {'class': 'price'}).contents[0]
    price_g = PRICE_REGEX.search(price)
    price_match = False
    if price_g:
        ret['price'] = int(price_g.group(1))
        if ret['price'] <= settings.max_rent:
            price_match = True

    #Neighborhood
    neighborhood = entry.find('small').contents[0]
    neighborhood = neighborhood.lower()
    neighborhood_match = False
    for n in settings.neighborhoods:
        if n in neighborhood:
            neighborhood_match = True

    ret['match'] = price_match and neighborhood_match and bed_match

    return ret

def email(matches):
    # params: From, To, Subject
    message = Message('sender@email.com', RECPIPENTS, "Scraper Results") 
    results = ''
    for listing in matches['match']:

        results.append("""

        {0}\tPrice: {1}
        Bedrooms: {2}
        {3}\n\n 

        """.format(matches.title,matches.price,
                    matches.bedroom,matches.link))

    message.body = results
    sender = Mailer('mail.server.net')
    sender.send(message)

def scrape():
    html = urllib2.urlopen(settings.url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    bq = soup.findAll('p', {'class': 'row'})

    for entry in bq:
        try:
            parsed = parse_entry(entry)
        except:
            print("\n+Failure: {0}").format(str(entry))
            continue

        if parsed['id'] in all_entries:
            continue
        all_entries[parsed['id']] = parsed
        if parsed['match']:
            print(str(parsed))
            email(parsed)
            #Notifier.notify(parsed['hook'], title='Craigslist', open=settings.notifierurl+parsed['link'], )

if __name__ == '__main__':
    while True:
        print 'Request sent ... '
        scrape()
        time.sleep(settings.period)
