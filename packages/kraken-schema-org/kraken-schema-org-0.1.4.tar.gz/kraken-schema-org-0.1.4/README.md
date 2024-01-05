
# kraken_schema_org
<definition>


## How to use

```
from kraken_schema_org import kraken_schema_org as k
```

## Most common methods

### Normalize record
Given a record, returns a fully normalized record
```
normalized_record = k.get_normalized_record(record)
```

## Class

### Get class / get schema
Returns schema.org schema for a given record_type
```
schema = k.get_class(record_type)
schema = k.get_schema(record_type)
```
### Get json schema
Returns json schema for a given record_type

```
json_schema = k.get_json_schema(record_type)
```

### Get summary keys (subset of most commonly used keys)
Returns the most commonly used keys for a given record_type
```
summary_keys = k.get_summary_keys(record_type)
```

### Get sample data
Returns sample record for a given record_type

```
sample_record = k.get_data(record_type)
```



## Property methods

### Get normalized key
```
normalized_key = k.get_key(key)
```

### Get all keys
```
keys = k.get_keys(record_type)
```

### Get json-ld type for a key
```
json_ld_type = k.key_get_jsonld_types(key)
```

### Get json type for a key
```
json_type = k.key_get_json_types(key)
```
### Get python type for a key
```
python_type = k.key_get_python_types(key)
```

### Get html type for a key
```
html_type = k.key_get_html_type(key)
```


### Normalize value for a key
```
normalized_value = k.get_normalized_value(key, value)
```

### Get localized key
```
localized_key = k.get_localized_key(key, 'EN-US')
```

### Convert key
Returns official key from given key (ex: last name -> familyName)
```
normalized_key = k.convert_key(key)
```

### Get key definition
```
defn = k.get_property_definition(key)
```

## Records

### Get record type
```
record_type = k.get_record_type(record)
```

### Get record id
```
record_id = k.get_record_id(record)
```

### Get record name
```
record_name = k.get_record_name(record)
```

### Get normalized record
```
normalized_record = k.get_normalized_record(record)
```


### Get summary record
```
summary_record = k.get_summary_record(record)
```
### Get localized record
```
localized_record = k.get_localized_record(record, 'EN-US')
```





## Legacy functions
FMethods provided to ensure backward compatibility. Avoid using
### Normalize @type

```
record_type = 'person'
normalized_type = k.normalize_type(record_type)
```

### Normalize key/attribute

```
key = 'givenname'
normalized_key = k.normalize_key(key)
```

### Normalize value or record

```
record = {"@type": "schema:WebPage", "schema:url": "https://www.test.com"}
normalized_record = k.normalize_record(record)
normalized_value = k.normalize_value(record_type: str, key: str, value: xx, strict: bool)

```

### Get keys/attributes for a given @type

```
record_type = 'person'
keys = k.get_keys(record_type)
```

### Get Datatypes for a given key

```
record_type = 'schema:Person'
key = 'schema:givenName'
datatypes = k.get_datatype(record_type, key)
```



### Normalize type

```
normalized_record_type = k.normalize_type(record_type)

```


