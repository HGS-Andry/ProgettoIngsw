from datetime import date , datetime
import hashlib

from DM_Postgre import DM_postgre

class Model(object):
    def __init__(self):
        self.id = " Model_ " + date.today().isoformat()
        print("|- creato model: "+self.id)
        self.dataMapper = DM_postgre()  

    
    def close(self):
        print("|- chiudiamo "+self.id)
        self.dataMapper.close()

    def registrazione(self, nome, cognome, mail, password):
        paswhash = hashlib.md5(password.encode()).hexdigest()
        # paswhash = p.hexdigest()
        #TODO controllo mail
        messaggio, result = self.dataMapper.registrazione( nome, cognome, mail, paswhash)
        return messaggio, result