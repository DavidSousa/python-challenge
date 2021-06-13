from collections import namedtuple, defaultdict

fieldNames = ['email', 'domain', 'company']
LeakedEmail = namedtuple('LeakedEmail', fieldNames)

class LeakedEmailsDB:
  
  def __init__(self, records):
    if not all([isinstance(record, LeakedEmail) for record in records]):
      raise ValueError('Provided leaked emails must be of type {}'.format(LeakedEmail.__name__))

    self.records = records
    
    self.lookups = {}
    for fieldName in fieldNames:
      lookup = self.lookups[fieldName] = defaultdict(list)
      for index, record in enumerate(self.records):
        value = getattr(record, fieldName)
        lookup[value].append(index)

  def get(self, **kwargs):
    if len(kwargs) != 1:
        raise ValueError('One argument is needed for the get method')

    field, value = kwargs.popitem()

    if field not in fieldNames:
        raise ValueError('Invalid field name')

    return tuple(self.records[i] for i in self.lookups[field].get(value, []))
