# A wiser hunt for apartments ...
### Small project I am working on to help me become the ultimate apartment hunter

### Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- $ sudo easy_install pip
- $ sudo pip install BeautifulSoup

### Install [pync's Notification Wrapper](https://github.com/setem/pync)
- Requires Mac OS X 10.8 or higher...
- $ sudo pip install pync

### Install [mailer](https://pypi.python.org/pypi/mailer/)
- $ sudo pip mailer

### Functional Requirements
- Parses out crucial information from listings and creates a digest for the recipient
- Only sends out newest listings since last digest

### Engineering Requirments
- Parse through RSS/XML feed, find desired information
- Utilize regex for information not easily accessed (eg not in kv pairs)
- Formatting parsed info in an HTML email and send to recipients
- Track listings through database (unimplemented)


### TODO:
- Retool parser for XML, not raw HTML
- Debug smtp
- Debug parsers
