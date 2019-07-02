from datetime import date , datetime
import hashlib
import string

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
        
    def addAutore(self, nomeaut):
        '''Aggiungi un autore al database'''
        if nomeaut != '':
            messaggio, result, idaut = self.dataMapper.addAutore(nomeaut)
            return messaggio, result, idaut
        else:
            return "Nome autore mancante", 1, None
            

    ########## GESTIONE CASA EDITRICE ############
    def getEdit(self):
        '''Fetcha tutte le case editrici '''
        messaggio, result, listaEdit = self.dataMapper.getEdit()
        return messaggio, result, listaEdit

    def addEdit(self, nomeedit):
        '''Aggiungi Casa Editrice'''
        if nomeedit != '':  
            messaggio, result, idedit = self.dataMapper.addEdit(nomeedit)
            return messaggio, result, idedit
        else:
            return "Nome editore mancante", 1, None

    
    ########## GESTIONE GENERE ############
    def getGenere(self, idgenere):
        '''Fetcha il genere con il nome dato'''
        if not idgenere:
            return "ID mancante", 0, None
        messaggio, result, listaGenere = self.dataMapper.getGenere(idgenere)
        return messaggio, result, listaGenere

    def getGeneri(self):
        '''Fetcha TUTTI i generi'''
        messaggio, result, listaGeneri = self.dataMapper.getGeneri()
        return messaggio, result, listaGeneri

    def addGenere(self, nomegenere, immaginegenere):
        '''Aggiungi Genere'''
        if nomegenere != '':    
            messaggio, result, idgenere = self.dataMapper.addGenere(nomegenere, immaginegenere)
            return messaggio, result, idgenere
        else:
            return "Nome del genere mancante", 1, None
    
    def modGenere(self, idgenere, nomegenere, immaginegenere):
        if idgenere or nomegenere or immaginegenere:
            if idgenere.isdigit():
                messaggio, result = self.dataMapper.modGenere(idgenere, nomegenere, immaginegenere)
            else:
                return "ID Genere errato", 0
        else:
            return "Campi non presenti", 0
        return messaggio, result

    def getLibriGenere(self, idgenere):
        if not idgenere:
            return "Genere mancante", 0, None
        messaggio, result, listaLibri = self.dataMapper.getLibriGenere(idgenere)
        return messaggio, result, listaLibri

    ########## GESTIONE LIBRI ##############
    def addLibro(self, isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idaut,idgenere):
        '''Aggiungi un libro al database. Ritorna il messaggio e result (0 errore, 1 effettuato) e isbn'''

        if (titolo != '' and datapubb != '' and prezzo != 0 and punti != 0 and posclas != 0 and idEdit != 0 and quant != 0 and idaut != '' and idgenere != ''):
            
            isbn.replace(' ','')
            if not isbn.isdigit():
                return "ISBN deve essere un valore numerico", 0, None
            
            if len(isbn) < 13:
                return "ISBN troppo corto", 0, None
            if len(isbn) > 13:
                return "ISBN troppo lungo", 0, None
            
            if not posclas.isdigit():
                return "Posizione classifica errata", 0, None
            if not punti.isdigit():
                return "Valore dei punti errato", 0, None
            if not prezzo.isdigit():
                return "Valore del prezzo errato", 0, None
            if not quant.isdigit():
                return "Quantità non accettabile", 0, None
            if not idEdit.isdigit():
                return "ID Editore errato", 0, None
            if not idaut.isdigit():
                return "ID Autore errato", 0, None
            if not idgenere.isdigit():
                return "ID Genere errato", 0, None

            messaggio, result, isbn = self.dataMapper.addLibro(isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idaut,idgenere)
            return messaggio, result, isbn
        else:
            return "Dati mancanti", 0, None

    def getLibro(self, isbn):
        '''Fetch il libro con isbn dato. Ritorna errore altrimenti'''
        if isbn != '' and len(isbn) == 13:
            messaggio, result, libro = self.dataMapper.getLibri([isbn]) #passo come lista per avere un solo libro
            return messaggio, result, libro[0] #prendo solo il primo della lista
        else:
            return "ISBN non corretto", 0, None

    def getLibri(self, listalibri):
        '''Trova i libri data una lista di isbn. Ritorna errore altrimenti'''
        if len(listalibri):
            messaggio, result, libri = self.dataMapper.getLibri(listalibri) 
            return messaggio, result, libri
        return "lista vuota", 0, None

    def modLibro(self, isbn, titolo, datapub, prezzo, punti, descr, immagine , idedit, quant, idaut, idgenere):
        '''modifica un libro a partire dai parametri passati'''

        if idord != '' and o_nomecognome != '' and o_indirizzo != '' and o_citta != '' and o_paese != '' and o_pagamento != '' and o_numtel != '':

            isbn.replace(' ','')
            if not isbn.isdigit():
                return "ISBN deve essere un valore numerico", 0, None
            
            if len(isbn) < 13:
                return "ISBN troppo corto", 0, None
            if len(isbn) > 13:
                return "ISBN troppo lungo", 0, None
            
            if not posclas.isdigit():
                return "Posizione classifica errata", 0, None
            if not punti.isdigit():
                return "Valore dei punti errato", 0, None
            if not prezzo.isdigit():
                return "Valore del prezzo errato", 0, None
            if not quant.isdigit():
                return "Quantità non accettabile", 0, None
            if not idEdit.isdigit():
                return "ID Editore errato", 0, None
            if not idaut.isdigit():
                return "ID Autore errato", 0, None
            if not idgenere.isdigit():
                return "ID Genere errato", 0, None

            messaggio, result = self.dataMapper.modLibro(isbn, titolo, datapub, prezzo, punti, descr, immagine , idedit, quant, idaut, idgenere)
        else:
            return "Parametri non corretti", 0

        return messaggio, result

    def aggiornaClassifica(self, isbn, posclas):
        '''Aggiorna la posizione in classifica del libro selezionato e aggiorna la data di aggiornamento. Valore compreso tra 1 e 11 '''
        if not isbn or not posclas:
            return "Valori non presenti", 0

        if posclas.isdigit():
            posclas = int(posclas)
            if posclas > 11:
                return "Valore troppo alto, per settare un libro fuori dalla classifica si deve impostare a 11", 0
            elif posclas < 1:
                return "Valore troppo basso, la prima posizione disponibile è 1", 0
            else:
                messaggio, result = self.dataMapper.aggiornaClassifica(isbn, posclas)
                return messaggio, result
        

    ########## GESTIONE RICERCA LIBRI ##############
    def searchBooks(self, word):
        '''Ricerca nel database dei libri che possano collimare con la ricerca data'''
        if '*' in word:
            word.replace('*', ' ')

        stringaControllo = "'#$%&\()*+/:;<=>?@[\\]^_`{|}~"
        
        wordCopy = ''
        space = ' '
        for i in word:
            if i in stringaControllo:
                i = space
            wordCopy += i

        word = wordCopy

        if word != '':
            messaggio, result, listaLibri = self.dataMapper.searchBooks(word)
            return messaggio, result, listaLibri
        else:
            return "Il campo di ricerca è vuoto", 1, None

    
    ########## GESTIONE CLASSIFICHE ##############
    def getClassificaPerGenere(self, idgenere):
        '''Fetch della classifica.'''
        if idgenere != '':
            messaggio, result, listaLibri = self.dataMapper.getClassificaPerGenere(idgenere)
            return messaggio, result, listaLibri
        else:
            return "ID genere non corretto", 0, None
                
    ############# GESTIONE ORDINE #################
    def salvaOrdine(self, idord, o_nomecognome, o_indirizzo, o_citta, o_provincia, o_paese, o_numtel, o_cap, o_pagamento):
        ''' Nel momento in cui l'utente finalizza l'acquisto, per ogni libro acquistato si genera una relazione
        in cui rel_prezzo=lib.prezzo, rel_punti=lib.punti, dopo aver controllato che la quantità del magazzino
        sia sufficiente da poter soddisfare l'ordine. Se il controllo fallisce, faccio rollback() e annullo 
        l'acquisto.
        Se il controllo va a buon fine per ogni libro, setto il ordine.stato='salvato', o_* = ordine.o_*, 
        dataora=now()
        ritorna il prezzo tot e punti tot
        '''

        if idord != '' and o_nomecognome != '' and o_indirizzo != '' and o_citta != '' and o_paese != '' and o_pagamento != '' and o_numtel != '':
            messaggio, result, prezzopunti = self.dataMapper.salvaOrdine(idord, o_nomecognome, o_indirizzo, o_citta, o_provincia, o_paese, o_numtel, o_cap, o_pagamento)
            return messaggio, result, prezzopunti
        else:
            return "Parametri ordine non accettati", 0, None



    def creaOrdine(self, listaLibri):
        ''' Metodo che viene chiamato solo se l'utente non è registrato.
        Genero un idord con dataMapper.creaCarrello(''). Per ogni libro di listaLibri aggiungo il libro al carrello suddetto
        con addCart(idord, isbn, quant).
        Ritorno idord
        '''
        if not listaLibri:
            return "Lista libri vuota", 0, None

        messaggio, result, idord = self.dataMapper.creaCarrello(None)
        if result == 0:
            return messaggio, result, None

        if listaLibri != None:
            for libro in listaLibri:
                messaggio, result = self.dataMapper.addCart(idord, libro, listaLibri[libro])
            return messaggio, result, idord
        else:
            return messaggio, result, None
           

    def setStatoOrdine(self, idord, stato):
        ''' Setto lo stato dell'ordine tramite il parametro 'stato' '''
        if not idord.isdigit() or not stato.isaplpha():
            messaggio, result = self.dataMapper.setStatoOrdine(idord, stato)
        return messaggio, result
    
    
    def getOrdini(self):
        ''' Ritorna tutti gli ordini in stato diverso da 'carrello' '''
        messaggio, result, listaordini = self.dataMapper.getOrdini()
        return messaggio, result, listaordini

    def annullaOrdine(self, idord):
        ''' Setta lo stato dell'ordine corrispondente al campo idord ad 'annullato' e per ogni libro dell'ordine
        riaggiunge la quantità ordinata nel magazzino. 
        Non ritorna parametri. '''
        if not idord:
            return "ID ordine non presente", 0
        messaggio, result = self.dataMapper.annullaOrdine(idord)
        return messaggio, result
    


    ###################################
    ##  Login - Logout - registrazione
    ###################################

    def registrazione(self, nome, cognome, email, password):
        '''Gestisce la registrazione. La password verrà codificata con md5. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        if '' not in (nome, cognome, email, password): #controllo che le variabili non siano vuote
            paswhash = hashlib.md5(password.encode()).hexdigest()
            
            #Controllo mail:
            stringaControllo="!\"#$%&\'()*+,./:;<=>?[\\]^`{|}~"
            for e in email:
                if e in stringaControllo:
                    return "La email non può contenere caratteri speciali", 0, None
            if not '@' in email:
                return "%s non è una mail valida"%email, 0

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
            if idA.isdigit():
                paswhash = hashlib.md5(password.encode()).hexdigest()
                messaggio, result, idAdmin, nome = self.dataMapper.loginadmin(idA, paswhash)
                return messaggio, result, idAdmin, nome
            else:
                return "Email errata.", 0, None, None
        else:
            return "Dati mancanti", 0, None, None

    #################################
    ##  PROFILO UTENTE / ADMIN
    #################################
    def getUtente(self, librocard):
        '''Dato Librocard ritorna una lista con le informazioni personali di un utente'''
        if not librocard:
            return "Librocard non presente", 0, None
        messaggio, result, utente = self.dataMapper.getUtente(librocard)
        return messaggio, result, utente
    
    def getOrdiniUtente(self, librocard):
        '''Dato Librocard ritorna una lista con gli ordini dell'utente TRANNE QUELLI CON STATO CARRELLO
           Restituisce tot punti, tot prezzo per ogni ordine'''
        if not librocard:
            return "Librocard non presente", 0, None
        messaggio, result, ordini = self.dataMapper.getOrdiniUtente(librocard)
        return messaggio, result, ordini
    
    def getOrdine(self, idord):
        '''Dato idord ritorna i dettagli dell'ordine selezionato quindi ritorna tutti i libri che ci sono
           nell'ordine, JOIN con rel_ordine, JOIN con case_editrici, JOIN con autori, JOIN con generi'''

        stringaControllo="!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        for i in idord:
            if i.isalpha() or i in stringaControllo:
                return "ID ordine deve essere composto da valori numerici", 0, None

        messaggio, result, ordine = self.dataMapper.getOrdine(idord)
        return messaggio, result, ordine

    def getLibriInOrd(self, idord):
        if idord:
            messaggio, result, libri = self.dataMapper.getLibriInOrd(idord)
        else:
            return "ID ordine non presente", 0, None
        return messaggio, result, libri

    def addIndirizzo(self, librocard, nomecognome, indirizzo, citta, provincia, paese, numtel, cap ):
        '''Salva un indirizzo associato ad una librocard'''
        
        stringaControllo = "!\"#$%&()*+:;<=>?@[\\]^_`{|}~"
        if idindirizzo != '' and nomecognome != '' and indirizzo != '' and citta != '' and paese != '' and numtel != '':
            if nomecognome.isalpha() and citta.isalpha() and paese.isalpha() and numtel.isdigit():
                for i in indirizzo:
                    if i in stringaControllo:
                        return "Caratteri non consentiti in Indirizzo", 0
                    else:
                        messaggio, result, idindirizzo = self.dataMapper.modIndirizzo(idindirizzo, nomecognome, indirizzo, citta, provincia, paese, numtel, cap)
        return messaggio, result, idindirizzo
    
    def getIndirizzi(self, librocard):
        '''Ritorna la lista di indirizzi dell'utente dato la sua librocard   '''
        if librocard:
            messaggio, result, listaindirizzi = self.dataMapper.getIndirizzi(librocard)
        else:
            return "Librocard non presente.", 0, None
        return messaggio, result, listaindirizzi

    def  getIndirizzo(self, idindirizzo):
        '''Ritorna i dettagli dell'indirizzo dato idindirizzo   '''
        if idindirizzo:
            messaggio, result, indirizzo = self.dataMapper.getIndirizzo(idindirizzo)
        else:
            return "ID indirizzo non presente.", 0, None
        return messaggio, result, indirizzo

    def modIndirizzo(self, idindirizzo, nomecognome, indirizzo, citta, provincia, paese, numtel, cap ):
        '''Dato idindirizzo e parametri modifica l'indirizzo nel database'''
        stringaControllo = "!\"#$%&()*+:;<=>?@[\\]^_`{|}~"
        if idindirizzo != '' and nomecognome != '' and indirizzo != '' and citta != '' and paese != '' and numtel != '':
            if nomecognome.isalpha() and citta.isalpha() and paese.isalpha() and numtel.isdigit():
                for i in indirizzo:
                    if i in stringaControllo:
                        return "Caratteri non consentiti in Indirizzo", 0
                    else:
                        messaggio, result = self.dataMapper.modIndirizzo(idindirizzo, nomecognome, indirizzo, citta, provincia, paese, numtel, cap )
        return messaggio, result

    def eliminaIndirizzo(self, idindirizzo):
        '''Dato idindirizzo elimina l'indirizzo dal database'''
        if idindirizzo:
            messaggio, result = self.dataMapper.eliminaIndirizzo(idindirizzo)
        else:
            return "ID indirizzo non presente", 0
        return messaggio, result

    def modificaUtente(self, librocard, nome, cognome, email):
        '''Data la librocard e i dati da variare dell'utente si procede alla modifica '''
       
        if nome.isalpha() and cognome.isalpha():
            stringaControllo="!\"#$%&\'()*+,/:;<=>?[\\]^`{|}~"
            for e in email:
                if e in stringaControllo:
                    return "La email non può contenere caratteri speciali", 0
            if not '@' in email:
                return "%s non è una mail valida"%email, 0
            
            messaggio, result = self.dataMapper.modificaUtente(librocard, nome, cognome, email)
        else:
            return "Nome e Cognome non possono contenere numeri o caratteri"
        
        return messaggio, result
    
    def modificaPasswordUtente(self, librocard, password):
        '''Data la librocard dell'utente, se ne modifica la password. Per ovvie ragioni non vengono fatti controlli
           sulla password. '''
        paswhash = hashlib.md5(password.encode()).hexdigest()
        messaggio, result = self.dataMapper.modificaPasswordUtente(librocard, passwhash)
        return messaggio, result

    #################################
    ##  carrello
    #################################
    def getCarrello(self, librocard):
        #cerco se ho il carreello, altrimenti lo creo TODO controlli
        messaggio, result, idord = self.dataMapper.getCarrello(librocard)
        if not result:
            messaggio2, result, idord = self.dataMapper.creaCarrello(librocard)
            return messaggio + messaggio2, result, idord
        return messaggio, result, idord
    
    def addCart(self, idord, isbn, quant):
        #provo ad inserirslo, se esiste già lo modifico
        messaggio, result = self.dataMapper.addCart(idord, isbn, quant)
        if not result:
            messaggio, result = self.dataMapper.modLibInOrd(idord, isbn, None, None, quant)
        return messaggio, result
    
    def isInCart(self, idord, isbn):
        messaggio, result, dettRelLibOrd = self.dataMapper.getRelLibInOrd(idord, isbn)
        return messaggio, result, dettRelLibOrd

    def remLibOrd(self,idord,isbn):
        '''Rimuove il libro dato dall'ordine '''
        messaggio, result = self.dataMapper.remLibOrd(idord,isbn)
        return messaggio, result