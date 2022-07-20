from collections.abc import MutableMapping
import json
import sys

class JsonHash:
    '''
    JsonHash is a Class enabling the processing and querying of JSON data.
    ROUGH example of how we could work with the hash table.
    '''
    def __init__(self, json_data, p_sparse=False):
        # store json
        # self.json_data = json_data
        # attribute to store the p_sparse parameter
        self.make_sparse = p_sparse
        # placeholder for query results
        self.results = []
        # hash the json object
        self.hash_table = self.hash_json(json_data)
        # reference for parsing the hash key
        # TODO: rename to json_map
        self.levels =   {
                        "member_id": 1,
                        "member_age": 1,
                        "member_sex": 1,
                        "claim": 1,
                        "claim_id": 3,
                        "claim_type": 3,   
                        "type_of_bill": 3,
                        "admission_date": 3,
                        "discharge_date": 3,
                        "taxonomy_code": 3,
                        "place_of_service": 3,
                        "principle_diagnosis": 3,
                        "diagnosis_codes": 3,
                        "drg": 3,  
                        "drg_severity": 3,
                        "drg_type": 3,
                        "claim_line": 3,
                        "line_number": 5,
                        "from_date": 5,
                        "thru_date": 5,
                        "revenue_code": 5,
                        "procedure_code": 5,
                        "ndc_code": 5,
                        "quantity": 5,
                        "allowed_amount": 5
                    }

    def hash_json(self, p_dictionary, p_parent_key=False, p_sparse=False):
        '''
        Gary's awesome JSON hashing function
        '''
        _items = []
        for _key, _value in p_dictionary.items():
            _new_key = str(p_parent_key) + '.' + _key if p_parent_key else _key
            if isinstance(_value, MutableMapping):
                # it's a dictionary
                if not _value.items():
                    # check for empty dictionary
                    _items.append((_new_key, None))
                else:
                    # not empty, recurse!
                    _items.extend(self.hash_json(_value, _new_key, self.make_sparse).items())
            elif isinstance(_value, list):
                # it's a list, so check to see if it's [not] empty
                if len(_value):
                    for _k, _v in enumerate(_value):
                        _items.extend(self.hash_json({str(_k): _v}, _new_key, self.make_sparse).items())
                else:
                    # empty list
                    _items.append((_new_key, None))
            else:
                # not dict or list, so append key, value
                if self.make_sparse is True and _value is None:
                        continue           
                _items.append((_new_key, _value))
        return dict(_items)

    def describe_json(self):
        '''
        OPTIONAL
        TODO: Pretty print the structure of the JSON object (json_map)
        '''
        return 

    def trimLastElement(self, key):
        '''
        Removes the last element from the hash key
        '''
        _new_key = key.split('.')[:-1]
        return '.'.join(_new_key)

    def mapStr(self, obj):
        '''
        Coerce list items to str
        '''
        return [i for i in map(str, obj)]

    def getLastElement(self, key): 
        '''
        Returns the last element of a key
        '''
        return key.split('.')[-1]


    def getKeyDepth(self, key):
        '''
        returns depth of a given key
        This is messy and highly specific to this work. We would need labels for the 
        various levels of the JSON to do this dynamically.
        '''
        _key = key.split('.')
        
        # if the last element is numeric, it's an array index, so go further back in the key
        # ex ['contents', '0', 'claim', '4', 'claim_line', '3', 'diagnosis_codes', '5']
        if _key[-1].isnumeric():
            return _key[-4]
        else:
            return _key[-3].replace('contents', 'member')

    def getMemberComponent(self, key):
        ''''
        Get member portion of key
        '''
        _key = key.split('.')
        try:
            return '.'.join(_key[:2])
        except IndexError:
            return None

    def getClaimComponent(self, key):
        ''''
        Get claim portion of key
        '''
        _key = key.split('.')
        try:
            return '.'.join(_key[:4])
        except IndexError:
            return None        

    def getClaimLineComponent(self, key):
        ''''
        Get claim line portion of key
        '''
        _key = key.split('.')
        try:
            return '.'.join(_key[:6])
        except IndexError:
            return None                        

    def getKeyInfo(self, key):
        '''
        key: a key from the hash table
        returns: a dictionary with information about the key of the form:
            {
                key: 'contents.0.claim.3.claim_line.3.procedure_code,
                depth: 'claim_line',
                member: 'contents.0',
                claim: 'contents.0.claim.3',
                claim_line: 'contents.0.claim.3.claim_line.3'
            }
        TODO: Once we have a schema generator, let's generalize this using the schema.
        '''
        _depth = self.getKeyDepth(key)
        return {
            'key': key,
            'depth': _depth,
            'member': self.getMemberComponent(key), # every key has a member component
            'claim': self.getClaimComponent(key) if _depth.startswith('claim') else None,
            'claim_line': self.getClaimLineComponent(key) if _depth == 'claim_line' else None
            }

    def find_or(self, search_values):
        '''
        values: dictionary of the form {data_element: [list of associated values]}
        Return a dictionary of the form: 
                {
                    data_element: [
                        {
                            key: 'contents.0.claim.5.claim_id',
                            depth: 'claim',
                            member: 'contents.0',
                            claim: 'contents.0.claim.5',
                            claim_line: None
                        }
                    ]
                }
        TODO: Can we chain this with another call to find?
                EX: find professional claims with 99214 and a specific taxonomy code
                    find(['P']).find(['99214']).find(['207QA0000X'])
        '''
        if not isinstance(search_values, dict):
            raise TypeError('Malformed parameter: search_values must be dict like object')
        
        # initialize dict with the keys = keys from the search_values dict
        _results_dict = {el: [] for el in search_values.keys()}
        
        # loop through the search criteria and build the _return_dict
        for _key, _values in search_values.items():
            # This sacrifices a lot of readability and may need to be refactored
            _results_dict.update({_key: [self.getKeyInfo(_k) for _k, _v in self.hash_table.items() if str(_v) in self.mapStr(_values) if self.getLastElement(_k)==_key]})

        return _results_dict

    def find_and(self, search_values):
        '''
        Find the intersection of keys in the results object
        Ex: 
        Matches the professional claim query:
            {'contents.0.claim.35.claim_type': 'P'}
        Matches the Office Visit query:
            {'contents.0.claim.35.claim_line.0.procedure_code': '99214'}
        Intersecting portion of the key is this claim for this member. It can be used
        to find the corresponding service date or provider taxonomy, etc.
            {'contents.0.claim.35}
        
        '''
        # obtain _results_dict from find_or method
        _results_dict = self.find_or(search_values)

        # initialize object to store all keys for matching
        _all_keys = {
            'member': [],
            'claim': [],
            'claim_line': []
        }

        # Example assuming 1 result per search criteria
        # Each item in the list is a set
        # 'member': []:
        # [{'contents.0'}, {'contents.0'}]

        # Pull out keys for each search criteria and store them as a set
        # in the object created above.
        # ex: 
        # { 'member': [set1, set2, set3], 
        #   'claim': [set1, set2, set3],
        #  ... }
        for key, values in _results_dict.items():
            _mbr_keys = []
            _clm_keys = []
            _clmln_keys = []
            for v in values:
                _mbr_keys.append(v['member'])
                _clm_keys.append(v['claim'])
                _clmln_keys.append(v['claim_line'])
            _all_keys['member'].append(set(_mbr_keys))
            _all_keys['claim'].append(set(_clm_keys))
            _all_keys['claim_line'].append(set(_clmln_keys))

        # Apply set intersection to identify keys that exist in all search results
        # first iteration: 
        #    all_keys['member'].pop().intersection(*_all_keys['member'])   
        for key in _all_keys.keys():
            _all_keys[key] = _all_keys[key].pop().intersection(*_all_keys[key])   

        return _all_keys

    def from_keys(self, values):
        '''
        values: list of values to search hash table for
        Return a subset of the hash table with the corresponding value
        TODO: Can we chain this with another call to from_values?
                EX: find professional claims with 99214 and a specific taxonomy code
                    find(['P']).find(['99214']).find(['207QA0000X'])
        '''
        self.results = self.find_or(values)
        return self

    def get_element(self, element):
        '''
        Return the desired data element; allows chaining with from_keys()
        This could accept a list.
        '''
        _results = []
        _ix = self.levels.get(element)
        _keys = set()
        for _key in self.results.keys():
            _parts = _key.split('.')[:_ix+1]
            # TODO: handle cases where we can't return the desired element
            _new_key = '.'.join(_parts + [element])
            # prevent duplicates in the output
            if _new_key not in _keys:
                _keys.add(_new_key)
                _results.append({_new_key: self.hash_table[_new_key]})
        return _results

if __name__ == '__main__':
    # Parameterize code
    data_path_parameter = sys.argv[1]

    with open(data_path_parameter, 'r') as f:
        members = json.load(f)

    table = JsonHash(members, p_sparse=True)

    inpatient_search_criteria = {
        'claim_type': ['I'],
        'type_of_bill': [str(i).zfill(4) for i in range(110, 130)], 
        'revenue_code': [str(i).zfill(4) for i in range(100, 220)] + [str(i).zfill(4) for i in range(1000, 1010)]
        }

    inpatient_results = table.find_and(inpatient_search_criteria)

    _api_output = {
        'member_id': [],
        'member_age': [],
        'admission_date': [],
        'discharge_date': [],
        'principle_diagnosis': []
        }

    for key, values in inpatient_results.items():
        if key == 'member':
            for v in values:
                # Include member_id 
                _api_output['member_id'].append(table.hash_table[v + '.member_id'])
                # Include member_age 
                _api_output['member_age'].append(table.hash_table[v + '.member_age'])
        if key == 'claim':
            for v in values:
                # Include admission_date
                _api_output['admission_date'].append(table.hash_table[v + '.admission_date'])
                # Include discharge_date
                _api_output['discharge_date'].append(table.hash_table[v + '.discharge_date'])
                # Include principle_diagnosis
                _api_output['principle_diagnosis'].append(table.hash_table[v + '.principle_diagnosis'])
    
    print(_api_output)