import os
import pkg_resources
import json
import pathlib


db = {}

class Kraken_db:

    def __init__(self, path='data/definitions.json'):
        """
        """
        self._db_path = path
        self._db = {}

        self._filepath = pkg_resources.resource_filename('kraken_schema_org', self._db_path)
        
        self._init_db()

        self.load()

    def __len__(self):
        return self.len()


    
    
    def get(self, record_id=None):
        '''
        '''
        if not record_id:
            return self._db
        
        return self._db.get(record_id, None)
    
    
    def post(self, record_id, record):
        """
        """
        
        if not self._db:
            self._db = {}

        self._db[record_id] = record
        self.dump()
        return


    def delete(self, record_id):
        """
        """
        self._db.pop(record_id)
        return
    
    def load(self):
        """
        """
        if not os.path.isfile(self._filepath):
            return False

        
        with open(self._filepath, 'r') as f:
            self._db = json.load(f)

        return True

    def dump(self):
        """
        """
        with open(self._filepath, 'w') as f:
            json.dump(self._db, f, indent=4, default=str)
    
        return
        

    def len(self):
        """
        """
        return len(self._db.keys())
    
    def drop(self):
        """
        """
        # Remove file
        
        file_to_rem = pathlib.Path(self._filepath)
        file_to_rem.unlink(missing_ok = True)
        return

    
    def _init_db(self):
        """
        """
        
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)

    