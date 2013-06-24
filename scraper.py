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

from config import settings

PRICE_REGEX = re.compile('\$([\d]+)')
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

    ret['match'] = price_match and neighborhood_match

    return ret


def scrape():
    html = urllib2.urlopen(settings.url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    bq = soup.findAll('p', {'class': 'row'})

    for entry in bq:
        try:
            parsed = parse_entry(entry)
        except:
            cprint("\n+Failure: " + str(entry), 'red')
            continue

        if parsed['id'] in all_entries:
            continue
        all_entries[parsed['id']] = parsed
        if parsed['match']:
            cprint(str(parsed), 'green')


if __name__ == '__main__':
    while True:
        scrape()
        time.sleep(settings.period)
