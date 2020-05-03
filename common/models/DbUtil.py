
from mongoengine import fields


from mongoengine.fields import *


"""
class Pets(EmbeddedDocument):
    name = StringField()

class Person(EmbeddedDocument):
    name = StringField()
    address = StringField()
    pets = ListField(EmbeddedDocumentField(Pets))

class Group(Document):
    name = StringField()
    members = ListField(EmbeddedDocumentField(Person))

g = Group()

update_document(g, {
  'name': 'Coding Buddies',
  'members': [
    {
      'name': 'Dawson',
      'address': 'Somewhere in Nova Scotia',
      'pets': [
        {
          'name': 'Sparkles'
        }
      ]
    },
    {
      'name': 'rednaw',
      'address': 'Not too sure?',
      'pets': [
        {
          'name': 'Fluffy'
        }
      ]
    }
  ]
})


"""


def field_value(field, value):
  '''
  Converts a supplied value to the type required by the field.
  If the field requires a EmbeddedDocument the EmbeddedDocument
  is created and updated using the supplied data.
  '''
  if field.__class__ in (ListField, SortedListField):
    # return a list of the field values
    return [
      field_value(field.field, item)
      for item in value]

  elif field.__class__ in (
    EmbeddedDocumentField,
    GenericEmbeddedDocumentField,
    ReferenceField,
    GenericReferenceField):

    embedded_doc = field.document_type()
    update_document(embedded_doc, value)
    return embedded_doc
  else:
    return value


def update_document(doc, data):
  ''' Update an document to match the supplied dictionary.
  '''
  for key, value in data.iteritems():

    if hasattr(doc, key):
        value = field_value(doc._fields[key], value)
        setattr(doc, key, value)
    else:
        # handle invalid key
        pass

  return doc
  


"""
Update a python doc
{u'communication': {u'mobile_phone': u'2323232323', 'email':{'primary' : 'email@example.com'}}}
>>{'set__communication__mobile_phone': u'2323232323', 'set__communication__email__primary': 'email@example.com'}


"""

def convert_dict_to_update(dictionary, roots=None, return_dict=None):
    """
    :param dictionary: dictionary with update parameters
    :param roots: roots of nested documents - used for recursion
    :param return_dict: used for recursion
    :return: new dict
    """
    if return_dict is None:
        return_dict = {}
    if roots is None:
        roots = []

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            roots.append(key)
            convert_dict_to_update(value, roots=roots, return_dict=return_dict)
            roots.remove(key)  # go one level down in the recursion
        else:
            if roots:
                set_key_name = 'set__{roots}__{key}'.format(
                    roots='__'.join(roots), key=key)
            else:
                set_key_name = 'set__{key}'.format(key=key)
            return_dict[set_key_name] = value

    return return_dict



#--------------------------------------------
"""
class Pets(EmbeddedDocument):
    name = StringField()

class Person(Document):
    name = StringField()
    address = StringField()
    pets = ListField(EmbeddedDocumentField(Pets))

person = Person()

data = {
    "name": "Hank",
    "address": "Far away",
    "pets": [
        {
            "name": "Scooter"
        }
    ]
}

update_document(person, data)

"""

def update_document(document, data_dict):

    def field_value(field, value):

        if field.__class__ in (fields.ListField, fields.SortedListField):
            return [
                field_value(field.field, item)
                for item in value
            ]
        if field.__class__ in (
            fields.EmbeddedDocumentField,
            fields.GenericEmbeddedDocumentField,
            fields.ReferenceField,
            fields.GenericReferenceField
        ):
            return field.document_type(**value)
        else:
            return value

    [setattr(
        document, key,
        field_value(document._fields[key], value)
    ) for key, value in data_dict.items()]

    return document
    
    
#----------------------------------------------------------------------
"""

"""



def mongo_to_dict(obj, exclude_fields):
    return_data = []

    if obj is None:
        return None

    if isinstance(obj, Document):
        return_data.append(("_id", str(obj.id)))

    for field_name in obj._fields:

        if field_name in exclude_fields:
            continue

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, list_field_to_dict(data)))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data, [])))
        elif isinstance(obj._fields[field_name], DictField):
            return_data.append((field_name, data))
        else:
            return_data.append((field_name, mongo_to_python_type(obj._fields[field_name], data)))

    return dict(return_data)


def list_field_to_dict(list_field):
    return_data = []

    for item in list_field:
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item, []))
        else:
            return_data.append(mongo_to_python_type(item, item))

    return return_data


def mongo_to_python_type(field, data):
    if isinstance(field, DateTimeField):
        return time.mktime(data.timetuple()) * 1000
    elif isinstance(field, ComplexDateTimeField):
        return field.to_python(data).isoformat()
    elif isinstance(field, StringField):
        return str(data)
    elif isinstance(field, FloatField):
        return float(data)
    elif isinstance(field, IntField):
        return int(data)
    elif isinstance(field, BooleanField):
        return bool(data)
    elif isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    else:
        return str(data)


## Example usage
if __name__ == "__main__":
    class Portfolio(Document):
        meta = {'collection': 'Portfolios'}
        PortfolioName = StringField()
        LastUpdateDate = DateTimeField(default=datetime.datetime.now())
        RecentActivity = ListField(default=[])


        @queryset_manager
        def to_dict(self, queryset):
            return mongo_to_dict(self, [])


