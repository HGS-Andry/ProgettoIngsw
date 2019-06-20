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

    #################################
    ##  Login - Logout - registrazione
    #################################

    def registrazione(self, nome, cognome, email, password):
        '''Gestisce la registrazione. La password verrà codificata con md5. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        if nome != '' and cognome != '' and email != '' and password != '': 
            paswhash = hashlib.md5(password.encode()).hexdigest()
            #TODO controllo mail
            messaggio, result, librocard = self.dataMapper.registrazione( nome, cognome, email, paswhash)
            return messaggio, result, librocard
        else:
            return "Dati mancanti", 0, None

    def login(self, email, password):
        '''Effettua il login dato utente e password. La password verrà codificata con md5. Ritorna messaggio, result (0 errore, 1 effettuato) e librocard. '''
        if email != '' and password != '': 
            paswhash = hashlib.md5(password.encode()).hexdigest()
            messaggio, result, librocard, nome = self.dataMapper.login(email, paswhash)
            return messaggio, result, librocard, nome
        else:
            return "Dati mancanti", 0, None, None