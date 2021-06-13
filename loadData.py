from utils.getUrls import getUrls
from utils.emails import validateEmail, getEmailDomain
from database import LeakedEmail

__dataLeaks = [{
  'company': 'Linkedin',
  'url': 'https://be-extra-datasets.s3-eu-west-1.amazonaws.com/dataleaks_sample/linkedinsample.txt'
}, {
  'company': 'Neopets',
  'url': 'https://be-extra-datasets.s3-eu-west-1.amazonaws.com/dataleaks_sample/neopetssample.txt'
}]

def loadData():
  results = getUrls([dataLeak['url'] for dataLeak in __dataLeaks]) 
  
  records = []

  for index, result in enumerate(results):
    emails = result.decode('utf-8').split('\n')
    for email in emails:
      if validateEmail(email):
        rec = LeakedEmail(email, getEmailDomain(email), __dataLeaks[index]['company'])
        records.append(rec)
  
  return records