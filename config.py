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

settings_dict = {
    'url': 'http://sfbay.craigslist.org/apa',
    'notifierurl': 'http://sfbay.craigslist.org/apa',
    'period': 21600,
    'bedrooms': '3br'
    'neighborhoods': [
        'oakland west',
        'emeryville',
        'downtown oakland',
        'oakland lake meritt / grand',
        'oakland north / temescal',
    ],
    'ignored_neighborhoods': [
        'Richmond',
        'San Leandro',
        'Orinda',
        'Hayward',
        'Albany',
        'Berkeley'
    ],
    'max_rent': 2000,
    'database': 'test.db' # not really sure where this is made or where it is implemented
}


class Settings(object):
    pass

settings = Settings()
for k, v in settings_dict.items():
    setattr(settings, k, v)
