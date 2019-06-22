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



    ########## GESTIONE AUTORI #############
    def getAutori(self):
        '''Fetcha tutti gli autori'''
        messaggio, result, listaAutori = self.dataMapper.getAutori()
        return messaggio, result, listaAutori
        
    def addAutore(self, nome):
        '''Aggiungi un autore al database'''
        if nome != '':
            messaggio, result, idaut = self.dataMapper.addAutore(nome)
            return messaggio, result, idaut
        else:
            return "Nome autore mancante", 1, None
            

    ########## GESTIONE CASA EDITRICE ############
    def getEdit(self):
        '''Fetcha tutte le case editrici '''
        messaggio, result, listaEdit = self.dataMapper.getEdit()
        return messaggio, result, listaEdit

    def addEdit(self, nome):
        '''Aggiungi Casa Editrice'''
        if nome != '':    
            messaggio, result, idedit = self.dataMapper.addEdit(nome)
            return messaggio, result, idedit
        else:
            return "Nome editore mancante", 1, None

    
    ########## GESTIONE GENERE ############
    def getGenere(self, idgenere):
        '''Fetcha il genere con il nome dato'''
        messaggio, result, listaGenere = self.dataMapper.getGenere(idgenere)
        return messaggio, result, listaGenere

    def getGeneri(self):
        '''Fetcha TUTTI i generi'''
        messaggio, result, listaGeneri = self.dataMapper.getGeneri()
        return messaggio, result, listaGeneri

    def addGenere(self, nome, immagine):
        '''Aggiungi Genere'''
        if nome != '':    
            messaggio, result, idgenere = self.dataMapper.addGenere(nome, immagine)
            return messaggio, result, idgenere
        else:
            return "Nome del genere mancante", 1, None
    
    def modGenere(self, idgenere, nome, immagine):
        messaggio, result = self.dataMapper.modGenere(idgenere, nome, immagine)
        return messaggio, result
       
    ########## GESTIONE LIBRI ##############
    def addLibro(self, isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idaut,idgenere):
        '''Aggiungi un libro al database. Ritorna il messaggio e result (0 errore, 1 effettuato) e isbn'''
        if (isbn != '' and titolo != '' and datapubb != '' and prezzo != 0 and punti != 0 and posclas != 0 and idEdit != 0 and quant != 0 and idaut != '' and idgenere != ''):
            #TODO controllo 
            messaggio, result, isbn = self.dataMapper.addLibro(isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idaut,idgenere)
            return messaggio, result, isbn
        else:
            return "Dati mancanti", 0, None

    def getLibro(self, isbn):
        '''Fetch il libro con isbn dato. Ritorna errore altrimenti'''
        if isbn != '' and len(isbn) == 13:
            messaggio, result, libro = self.dataMapper.getLibro(isbn)
            return messaggio, result, libro
        else:
            return "ISBN non corretto", 0, None

    
    ########## GESTIONE CLASSIFICHE ##############
    def getClassificaPerGenere(self, idgenere):
        '''Fetch della classifica.'''
        if idgenere != '':
            messaggio, result, listaLibri = self.dataMapper.getClassificaPerGenere(idgenere)
            return messaggio, result, listaLibri
        else:
            return "ID genere non corretto", 0, None


    #################################
    ##  Login - Logout - registrazione
    #################################

    def registrazione(self, nome, cognome, email, password):
        '''Gestisce la registrazione. La password verrà codificata con md5. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        if '' not in (nome, cognome, email, password): #controllo che le variabili non siano vuote
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
    
    def loginadmin(self, idA, password):
        '''Effettua il login per l'amministratore dato id e password. La password verrà codificata con md5. Ritorna messaggio, result (0 errore, 1 effettuato) e idAdmin. '''
        if idA != '' and password != '': 
            paswhash = hashlib.md5(password.encode()).hexdigest()
            messaggio, result, idAdmin, nome = self.dataMapper.loginadmin(idA, paswhash)
            return messaggio, result, idAdmin, nome
        else:
            return "Dati mancanti", 0, None, None