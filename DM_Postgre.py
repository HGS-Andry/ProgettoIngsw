import psycopg2.extras
from configparser import ConfigParser

class DM_postgre():
    __server = __db = __db4Log = __user = __password = __dbCon =__db4LogCon =None
    __nIstanze = 0

    @classmethod
    def __open(cls):
        Config = ConfigParser() 
        Config.read("server.ini")  #leggo il file server.ini

        #Inizializzo le variabili della connessione dal file server.ini
        cls.__server = Config["server"]["server"]               #ip server
        cls.__db =Config["server"]["db"]                        #database principale
        cls.__db4Log = Config["server"]["db4log"]               #database per il log
        cls.__user = Config["server"]["user"]                   #user
        cls.__password = Config["server"]["password"]           #password
        cls.__dbCon = None # La connessione è condivisa !       #connessione database principale
        cls.__db4LogCon = None # La connessione è condivisa !   #connessione database log
        cls.__nIstanze = 0                                      #istanze connessione

        # creiamo la connessione se non esiste
        if cls.__dbCon is None :
            try :
                cls.__dbCon = psycopg2.connect( host = cls.__server, database = cls.__db , user = cls.__user , password = cls.__password )
                cls.__dbCon.set_session( readonly = False, autocommit = True ) # Connessione di lettura condivisa
                print("|-- Connection to database " + cls.__db + " created .")
            except psycopg2.OperationalError as err:
                print("|-- 1) Error connecting to PostgreSQL DBMS at %s. nDetails : %s." %( cls.__server , err))
                cls.__dbCon = cls.__db4LogCon = None
                exit()
            print("|-- New connection opened .")
            return " New connection opened ."
        print("|--Connection already opened .")
        return " Connection already opened ."

    @classmethod
    def __close(cls):
        if cls.__nIstanze == 0 and cls.__dbCon is not None :
            cls.__dbCon.close()
            # cls.__db4LogCon.close()
            print("|-- Connection closed .")
            cls.__dbCon = cls.__db4LogCon = None

    @classmethod
    def __cursor(cls):
        """ Ritorna un cursore che restituisce dict invece di tuple per ciascuna riga di una select ."""
        print('|-- Richiesta cursore da:'+str(cls.__dbCon))
        return cls.__dbCon.cursor( cursor_factory = psycopg2.extras.DictCursor )

    # @classmethod
    # def __cursor4log(cls):
    #     """ Ritorna un cursore per scrivere nel database cls.__db4Log ."""
    #     print("-- Richiesta cursore")
    #     return cls.__db4LogCon.cursor()

    def __init__( self ):
        DM_postgre.__open()
        DM_postgre.__nIstanze += 1

    def close( self ):
        """ Chiude in modo esplicito la connessione , se non ci sono altre istanze attive """
        self.__del__()

    def __del__( self ):
        DM_postgre.__nIstanze -= 1
        print('|-- si chiude')
        DM_postgre.__close()




    #################################
    ##  Query getAutori (model present)
    #################################
    def getAutori(self):
        '''Ricerca l'autore'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM autori")
                return "Autori Fetchati", 1 , list(cur) #ritorno l'isbn
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    #################################
    ##  Query addAutore (model present)
    #################################
    def addAutore(self, nomeaut):
        '''Registra l'autore nuovo. Ritorna messaggio e result (0 errore, 1 effettuato) e idaut'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO autori (nomeaut) values(%s) RETURNING idaut", (nomeaut,))
                idaut = list(cur)[0]['idaut']
                return "Autore inserito.", 1 , idaut #ritorno l'autore
            except psycopg2.IntegrityError as err: #errore Integrità, libro già presente
                print(str(err))
                if err.pgcode =='23505': #UniqueViolation
                    return "Autore già presente nel DataBase", 0, None
                return str(err), 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  Query getEdit (model present)
    #################################
    def getEdit(self):
        '''Fetcha le Case Editrici'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM case_editrici")
                return "Editrici Fetchate", 1 , list(cur) #ritorno la lista di case editrici
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    #################################
    ##  Query AddEdit (model present)
    #################################
    def addEdit(self, nomeedit):
        '''Registra la casa editrice nuova. Ritorna messaggio e result (0 errore, 1 effettuato) e idEdit'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO case_editrici (nomeedit) values(%s) RETURNING idedit", (nomeedit,))
                idedit = list(cur)[0]['idedit']
                return "Editore inserito.", 1 , idedit #ritorno la casa editrice
            except psycopg2.IntegrityError as err: #errore Integrità, libro già presente
                print(str(err))
                if err.pgcode =='23505': #UniqueViolation
                    return "Editore già presente nel DataBase", 0, None
                return str(err), 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    


    #################################
    ##  Query getGenere (model present)
    #################################
    def getGenere(self, idgenere):
        '''Fetcha il genere'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM generi where idgenere=%s", (idgenere,))
                genere = list(cur)[0]
                if genere:
                    return "Genere Fetchato", 1 , genere #ritorno il genere singolo
                else:
                    return ("Il genere con id %s non è presente nel Database" % (idgenere))
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    #################################
    ##  Query getGeneri (model present)
    #################################
    def getGeneri(self):
        '''Fetcha TUTTI i generi'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM generi ORDER BY(nomegenere)")
                return "Generi fetchati", 1 , list(cur) #ritorno la lista dei generi
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    #################################
    ##  Query addGenere (model present)
    #################################
    def addGenere(self, nomegenere, immaginegenere):
        '''Registra il genere. Ritorna messaggio e result (0 errore, 1 effettuato) e idgenere'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO generi (nomegenere, immaginegenere) values(%s,%s) RETURNING idgenere", (nomegenere,immaginegenere))
                idgenere = list(cur)[0]['idgenere']
                return "Genere inserito.", 1 , idgenere #ritorno il genere
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  Query modGenere (model present)
    #################################
    def modGenere(self, idgenere, nomegenere, immaginegenere):
        '''Modifica il genere. Ritorna messaggio e result (0 errore, 1 effettuato)'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE generi SET nomegenere = %s, immaginegenere = %s WHERE idgenere = %s", (nomegenere,immaginegenere,idgenere))
                return "Genere modificato.", 1 
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    
    ########################################
    ##  Query getLibriGenere (model present)
    ########################################
    def getLibriGenere(self, idgenere):
        '''Ritorna la lista dei libri ordinata per classifica e nome appartenenti al genere dato'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * from libri JOIN autori ON libri.idaut = autori.idaut JOIN generi ON libri.idgenere = generi.idgenere JOIN case_editrici ON libri.idedit = case_editrici.idedit WHERE generi.idgenere = '%s' ORDER BY libri.posclas, libri.titolo"%idgenere)
                listaLibri = list(cur)
                return "Classifica per genere organizzata con successo.", 1, listaLibri
            except Exception as err:
                print(str(err))
                return str(err), 0, None



    #################################
    ##  Query getLibro (model present)
    #################################
    def getLibri(self, isbn):
        '''Fetcha il libro con isbn da una lista di isbn, ritorna errore altrimenti'''
        with type( self ).__cursor() as cur:
            try:
                sql = "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere WHERE isbn IN %s "
                cur.execute(sql, (tuple(isbn),))
                libro = list(cur)
                if libro:
                    return "Libro Fetchato", 1 , libro #ritorno la casa editrice
                else:
                    return ("Il libro con ISBN %s non è presente nel Database" % (isbn))
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  Query addLibro (model present)
    #################################
    def addLibro(self, isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idAut, idgenere):
        '''Registra l'utente nuovo. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO libri (isbn, titolo, datapub, prezzo, punti, descr, posclas, dataAggClas, immagine , idEdit, quant,idAut,idgenere) VALUES(%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s,%s)", (isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant, idAut, idgenere))
                return "Libro inserito.", 1, isbn #ritorno l'isbn
            except psycopg2.IntegrityError as err: #errore Integrità, libro già presente
                print(err.__str__)
                if err.pgcode == '23503': #ForeignKeyViolation
                    return "Autore o Editore non presente nel database", 0
                if err.pgcode =='23505': #UniqueViolation
                    return "Libro già presente nel DataBase", 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None


    #################################
    ##  Query getClassificaPerGenere (model present)
    #################################
    def getClassificaPerGenere(self, idgenere):
        '''Fetcha la classifica dei libri per per genere'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM libri WHERE idgenere=%s and posclas < 11 ORDER BY posclas", (str(idgenere),))
                listaLibri = list(cur)
                return "Libri in classifica per genere fetchati", 1 , listaLibri #ritorno la lista richiesta
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    
    
    
    #################################
    ##  Query searchBooks (model present)
    #################################
    def searchBooks(self, word):
        '''Crea una lista di libri che contengono la parola richiesta in titolo/autore del libro'''
        with type( self ).__cursor() as cur:
            try:
                ###### MANIPOLO LA RICERCA PER ISOLARE PAROLE SINGOLE:
                wordlist = word.split()
                n = int(len(wordlist))
                


                ###### MANIPOLO LA RICERCA PER TOGLIERE PAROLE INUTILI O TROPPO CORTE
                temp = ''
                index = 0
                a = 0
                while index < n:
                    if temp != '':
                        index = 0
                        temp = ''
                    if len(wordlist[index]) < 5:
                        temp = wordlist.pop(index)
                        n=n-1
                    else:
                        index += 1


                query = ""
                if n > 1: 
                    # Inizio la selezione sui libri che potrebber essere contenuti nella parola di ricerca o in alcuni suoi pezzi
                    # unitamente ai risultati sugli autori, DEVO QUINDI CREARE PRIMA LA QUERY DINAMICAMENTE PER POI ESEGUIRLA.
    
                    # GENERAZIONE QUERY PER LIBRI SU "word" E "wordlist"
                    query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.titolo ~* '%s'  UNION  "%word       
                    for i in wordlist:
                        query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.titolo ~* '%s'  UNION  "%i

                    # AGGIUNTA QUERY PER AUTORI SU "word" E "wordlist"
                    query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idaut IN (   SELECT idaut FROM autori   WHERE nomeaut ~* '%s')  UNION  "%word
                    for i in wordlist:
                        query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idaut IN (   SELECT idaut FROM autori   WHERE nomeaut ~* '%s')  UNION  "%i
                        
                    # AGGIUNTA QUERY PER GENERI SU "word" E "wordlist"    
                    query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idgenere IN (   SELECT idgenere FROM generi   WHERE nomegenere ~* '%s')  UNION  "%word
                    for i in wordlist:
                        query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idgenere IN (   SELECT idgenere FROM generi   WHERE nomegenere ~* '%s')  UNION  "%i
                    
                    # AGGIUNTA QUERY PER EDITORE SU "word" E "wordlist"
                    query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idedit IN (   SELECT idedit FROM case_editrici   WHERE nomeedit ~* '%s')  UNION  "%word
                    for i in wordlist:
                        query += "SELECT * FROM libri  JOIN autori ON libri.idaut = autori.idaut  JOIN case_editrici ON libri.idedit = case_editrici.idedit  JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idedit IN (   SELECT idedit FROM case_editrici   WHERE nomeedit ~* '%s')  UNION  "%i

                    # TOLGO UNION DALLA FINE DELLA QUERY 
                    query = query[:-7]
                else:

                    #RICERCA SU LIBRI
                    query = "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere WHERE libri.titolo ~* '%s' UNION "%word
                    #RICERCA SU ISBN
                    query += "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere WHERE libri.isbn IN (  SELECT isbn FROM libri WHERE isbn = '%s') UNION "%word
                    #RICERCA SU AUTORI
                    query += "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idaut IN (  SELECT idaut FROM autori  WHERE nomeaut ~* '%s') UNION "%word
                    #RICERCA SU GENERI
                    query += "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idgenere IN (  SELECT idgenere FROM generi  WHERE nomegenere ~* '%s') UNION "%word
                    #RICERCA SU EDITORI                
                    query += "SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit JOIN generi ON libri.idgenere = generi.idgenere  WHERE libri.idedit IN (  SELECT idedit FROM case_editrici  WHERE nomeedit ~* '%s');"%word 
    
                #print(query,"\n")  
                

                cur.execute(query)
                listaLibri = list(cur)
                return "Ricerca Libri completata.", 1, listaLibri             
                                    
            except Exception as err:
                print(str(err))
                return str(err), 0, None
                    
                # ora che ho le liste dei possibili autori procedo con l'algoritmo sul titolo del libro
                
              

    #################################
    ##  Query modificaLibro 
    #################################
    def modLibro(self, isbn, titolo, datapub, prezzo, punti, descr, immagine , idedit, quant, idaut, idgenere):
        '''modifica un libro a partire dai parametri passati'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE libri\n\tSET titolo=%s, datapub=%s, prezzo=%s, punti=%s, descr=%s, immagine=%s, idedit=%s, quant=%s, idaut=%s, idgenere=%s\nWHERE isbn=%s", (titolo, datapub, prezzo, punti, descr, immagine, idedit, quant, idaut, idgenere, isbn))
                return "Libro Modificato con successo", 1
            except psycopg2.IntegrityError as err: #errore Integrità, libro già presente
                if err.pgcode == '23503': #ForeignKeyViolation
                    return "Autore o Editore non presente nel database", 0
            except Exception as err:
                print(str(err))
                return str(err), 0
    #################################
    ##  Query aggiornaClassifica
    #################################
    def aggiornaClassifica(self, isbn, posclas):
        '''Aggiorna la posizione in classifica del libro selezionato e aggiorna la data di aggiornamento.'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE libri\n\tSET posclas=%s, dataAggClas=NOW()\nWHERE isbn=%s", (posclas, isbn))
                return "Classifica aggiornata", 1
            except Exception as err:
                print(str(err))
                return str(err), 0        
                
    #################################
    ##  registrazione (model present)
    #################################
    def registrazione(self, nome, cognome, email, password):
        '''Registra l'utente nuovo. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO utenti (Nome, Cognome, email, Password, DataReg) VALUES(%s, %s, %s, %s, NOW()) RETURNING librocard;", (nome,cognome, email, password))
                librocard = list(cur)[0]['librocard']
                return "Utente Registrato.", 1 , librocard #ritorno l'id corrente
            except psycopg2.IntegrityError as err: #errore Integrità email già presente
                print(err.__str__)
                return "Email già inserita", 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  LOGIN (MODEL PRESENT)
    #################################
    def login(self, email, password):
        '''Controlla che email e password corrispondano nel database. Ritorna messaggio e result (0 errore, 1 effettuato), librocard e nome'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT Librocard, nome FROM utenti where email = %s AND password = %s", (email, password))
                if cur.rowcount:
                    result= list(cur)[0]
                    librocard = result['librocard']
                    nome = result['nome']     
                    return "Login effettuato.", 1, librocard, nome #ritorno l'id corrente e il nome
                else:
                    return "Email o password errate.", 0 , None, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None, None
    
    def loginadmin(self, idA, password):
        '''Controlla che idAdmin e password corrispondano nel database. Ritorna messaggio e result (0 errore, 1 effettuato), idAdmin e nome'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT idadmin, nome FROM amministratori where idadmin = %s AND password = %s", (idA, password))
                if cur.rowcount:
                    result= list(cur)[0]
                    idAdmin = result['idadmin']
                    nome = result['nome']     
                    return "Login effettuato.", 1, idAdmin, nome #ritorno l'id corrente e il nome
                else:
                    return "Email/id o password errate.", 0 , None, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None, None

    #################################
    ##  CARRELLO
    #################################
    def getCarrello(self, librocard):
        #cerco se ho il carreello TODO controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT idord FROM ordini where librocard = %s AND stato = 'carrello'", (librocard,))
                idord = list(cur)
                if idord:                    
                    return "carrello trovato", 1, idord[0]['idord']
                else:
                    return "carrello non trovato", 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def creaCarrello(self, librocard):
        #creo il carrello TODO controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO ordini (stato, librocard) VALUES ('carrello',%s) RETURNING idord", (librocard,))
                idord = list(cur)[0]['idord']
                return "Carrello creato", 1 , idord #ritorno l'id corrente
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  ADD CART
    #################################
    def addCart(self,idord, isbn, quant):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO rel_ord_lib(idord,isbn,rel_quant) VALUES (%s,%s,%s)", (idord, isbn, quant))
                return "Libro inserito nel carrello", 1 
            except Exception as err:
                print(str(err))
                return str(err), 0

    
    #################################
    ##  GESTIONE ORDINI
    #################################
    def salvaOrdine(self, idord, o_nomecognome, o_indirizzo, o_citta, o_provincia, o_paese, o_numtel, o_cap, o_pagamento):
        ''' Nel momento in cui l'utente finalizza l'acquisto, per ogni libro acquistato si genera una relazione
        in cui rel_prezzo=lib.prezzo, rel_punti=lib.punti, dopo aver controllato che la quantità del magazzino
        sia sufficiente da poter soddisfare l'ordine. Se il controllo fallisce, faccio rollback() e annullo 
        l'acquisto.
        Se il controllo va a buon fine per ogni libro, setto il ordine.stato='salvato', o_* = ordine.o_*, 
        dataora=now().
        Ritorna il prezzo tot e punti tot.
        Tutto ciò va eseguito in maniera atomica.
        '''
        with type( self ).__cursor() as cur:
            try:
                # Prendo isbn | ordinati 
                cur.execute("SELECT L.isbn, R.rel_quant, L.prezzo, L.punti FROM libri L\
                    JOIN rel_ord_lib R ON R.isbn=L.isbn\
                    JOIN ordini O ON O.idord=R.idord\
                    WHERE O.idord=%s"%idord)
                ordine=list(cur)
                
                # Per ogni libro presente nell'ordine faccio il check che il magazzino sia sufficiente
                for libro in ordine:
                    cur.execute("SELECT quant FROM libri WHERE isbn=%s",(libro[0],))
                    magazzino = list(cur)       # Salvo la quantità del magazzino del libro corrente
                    
                    if magazzino:
                        libriInMag = magazzino[0][0]
                    else:
                        return "Magazzino non fetchato, errore.", 1, None

                    isbn = libro[0]             # Salvo l' ISBN del libro
                    ordinati = libro[1]         # Salvo la quantità nel carrello del libro corrente
                    prezzoLibro = libro[2]      # Salvo il prezzo del singolo libro
                    puntiLibro = libro[3]       # Salvo i punti del singolo libro

                    if libriInMag < ordinati:    # check magazzino 
                        return "Magazzino insufficiente, ordine annullato", 1, None
                    
                    # Dato che il magazzino è sufficiente, aggiorno rel_quant, rel_prezzo, rel_punti
                    libriInMag = libriInMag - ordinati
                    prezzoTot = prezzoLibro * ordinati
                    puntiTot = puntiLibro * ordinati

                    # Query update relazione ordine-libri
                    cur.execute("UPDATE rel_ord_lib\
	                        SET rel_punti=%s, rel_prezzo=%s\
                            WHERE idord=%s and isbn=%s", (puntiTot, prezzoTot, idord, isbn) )

                    # Query update magazzino in libro
                    cur.execute("UPDATE libri\
                            SET quant=%s\
                            WHERE isbn=%s", (libriInMag, isbn))

                    
                # Query finale di update ordini con o_* = o_*
                cur.execute("UPDATE ordini\
                            SET dataora=now(), o_nomecognome=%s, o_indirizzo=%s, o_citta=%s, o_provincia=%s, o_paese=%s, o_numtel=%s, o_cap=%s, o_pagamento=%s \
                            WHERE idord=%s", (o_nomecognome, o_indirizzo, o_citta, o_provincia, o_paese, o_numtel, o_cap, o_pagamento, idord))

                prezzoPunti = [prezzoTot, puntiTot]

                # Cambio lo stato in 'salvato'
                #msg1, flag = self.setStatoOrdine(idord, 'salvato')
                #msg2 = "Ordine salvato con successo. " + msg1
                msg2 = "Ordine salvato con successo."
                cur.execute("UPDATE ordini SET stato='salvato' WHERE idord=%s"%idord)
                return msg2, 1, prezzoPunti

            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def setStatoOrdine(self, idord, stato):
        ''' Setto lo stato dell'ordine tramite il parametro 'stato'.
            Non ritorna parametri '''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE ordini SET stato=%s WHERE idord=%s", (stato, idord))
                return "Stato ordine aggiornato con successo", 1
            except Exception as err:
                print(str(err))
                return str(err), 0

    def getOrdini(self):
        ''' Ritorna tutti gli ordini in stato diverso da 'carrello' '''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM ordini WHERE stato <> 'carrello' ORDER BY dataora DESC")
                listaOrdini = list(cur)
                return "Ordini correttamente estratti", 1, listaOrdini
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def annullaOrdine(self, idord):
        ''' Setta lo stato dell'ordine corrispondente al campo idord ad 'annullato' e per ogni libro dell'ordine
        riaggiunge la quantità ordinata nel magazzino. 
        Non ritorna parametri. '''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT L.isbn, R.rel_quant FROM libri L JOIN rel_ord_lib R ON R.isbn=L.isbn JOIN ordini O ON O.idord=R.idord WHERE O.idord=%s"%idord)
                libri=list(cur)

                for l in libri:
                    cur.execute("UPDATE libri SET quant=quant+%s WHERE isbn=%s",(l[1], l[0]))

                cur.execute("UPDATE ordini SET stato='annullato' WHERE idord=%s"%idord)

                return "Ordine annullato con successo", 1
            except Exception as err:
                print(str(err))
                return str(err), 0

    #################################
    ##  GESTIONE RELAZIONE ORDINE
    #################################
    def modLibInOrd(self,idord, isbn, punti, prezzo, quant):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE rel_ord_lib SET rel_punti = %s , rel_prezzo = %s, rel_quant = %s WHERE idord = %s AND isbn = %s", ( punti, prezzo, quant, idord, isbn))
                return "Relazione libro in ordine modificata", 1 
            except Exception as err:
                print(str(err))
                return str(err), 0

    def getRelLibInOrd(self, idord, isbn):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM rel_ord_lib WHERE idord = %s AND isbn = %s", (idord, isbn))
                dettRelLibOrd = list(cur)
                if dettRelLibOrd:
                    return "Relazione libro in ordine tovata", 1 ,dettRelLibOrd[0]
                else:
                    return "Relazione libro in ordine non tovata", 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def getLibriInOrd(self, idord):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM rel_ord_lib AS R JOIN libri AS L ON R.isbn = L.isbn JOIN autori AS A ON L.idaut = A.idaut JOIN case_editrici AS C ON L.idedit = C.idedit WHERE idord = %s", (idord,))
                libri = list(cur)
                if libri:
                    return "Libri in ordine trovati", 1 ,libri
                else:
                    return "Libri in ordine %s non trovati"%(idord), 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def remLibOrd(self, idord,isbn):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("DELETE FROM rel_ord_lib WHERE idord = %s AND isbn = %s",(idord,isbn))
                return "Libro eliminato da questo ordine", 1
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    
    

    #################################
    ##  PROFILO
    #################################
    def getUtente(self, librocard):
        '''Dato Librocard ritorna una lista con le informazioni personali di un utente più totpunti'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT U.librocard, nome, cognome, email,datareg, SUM(rel_punti*rel_quant) AS totpunti FROM utenti U FULL JOIN ordini O ON U.librocard = O.librocard FULL JOIN rel_ord_lib R ON R.idord = O.idord WHERE U.librocard = %s AND O.stato <> 'annullato' GROUP BY (U.librocard)",(librocard,))
                utente = list(cur)
                if utente:
                    return "Utente tovato", 1 ,utente[0]
                else:
                    return "Utente non tovato", 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    
    def getOrdiniUtente(self, librocard):
        '''Dato Librocard ritorna una lista con gli ordini dell'utente TRANNE QUELLI CON STATO CARRELLO'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT O.idord, O.o_paese, O.o_numtel, O.o_citta, O.dataora, O.o_nomecognome,O.o_indirizzo,O.stato,\
                                    (SELECT sum(rel_prezzo) AS totprezzo FROM rel_ord_lib WHERE idord=R.idord) AS totprezzo,\
                                    (SELECT sum(rel_punti) AS totpunti FROM rel_ord_lib WHERE idord=R.idord) AS totpunti\
                                    FROM ordini O\
					                    LEFT JOIN rel_ord_lib R ON O.idord=R.idord\
					                    LEFT JOIN utenti U ON U.librocard=O.librocard\
				                    WHERE O.librocard=%s AND stato <> 'carrello'\
				                    GROUP BY O.idord, O.o_paese, O.o_numtel, O.o_citta,O.dataora,O.o_nomecognome,O.o_indirizzo,O.stato,totprezzo,totpunti\
				                    ORDER BY O.dataora DESC"%librocard)

                listaOrdini = list(cur)
                return "Ordini estratti con successo", 1, listaOrdini
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    

    def getOrdine(self, idord):
        '''Dato idord ritorna i dettagli dell'ordine selezionato quindi ritorna tutti i libri che ci sono
           nell'ordine, JOIN con rel_ordine, JOIN con case_editrici, JOIN con autori, JOIN con generi'''
        with type( self ).__cursor() as cur:
            try:

                cur.execute("SELECT idord FROM ordini where idord=%s"%idord)

                if not list(cur):
                    return "Ordine con ID %s non presente nel database"%idord, 0, None

                cur.execute("SELECT O.idord,O.stato,O.dataora,O.o_nomecognome,O.o_indirizzo,O.o_citta,O.o_provincia,\
		                            O.o_paese,O.o_numtel,O.o_cap,O.librocard,O.o_pagamento,\
		                            R.isbn,R.rel_punti,R.rel_quant,\
		                            (SELECT sum(rel_prezzo) AS totprezzo FROM rel_ord_lib WHERE idord=%s) AS totprezzo,\
		                            (SELECT sum(rel_punti) AS totpunti FROM rel_ord_lib WHERE idord=%s) AS totpunti\
		                            FROM ordini O\
			                            FULL JOIN rel_ord_lib R ON O.idord=R.idord\
                                    WHERE O.idord=%s and O.stato <> 'carrello'\
	                                GROUP BY (O.idord,R.idord,R.isbn)",(idord,idord,idord))

                ordine = list(cur)[0]
                return "Ordine estratto con successo", 1, ordine
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    
    def modificaUtente(self, librocard, nome, cognome, email):
        '''Data la librocard e i dati da variare dell'utente si procede alla modifica '''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE utenti SET nome=%s, cognome=%s, email=%s WHERE librocard=%s", (nome, cognome, email, librocard))
                return "Modifica profilo effettuata", 1
            except psycopg2.IntegrityError as err: #errore Integrità, libro già presente
                print(str(err))
                if err.pgcode =='23505': #UniqueViolation
                    return "Email già presente nel DataBase", 0, None
                return str(err), 0, None
            except Exception as err:
                print(str(err))
                return str(err), 0

    def modificaPasswordUtente(self, librocard, password):
        '''Data la librocard dell'utente, se ne modifica la password '''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE utenti SET password=%s WHERE librocard=%s", (password, librocard))
                return "Modifica password effettuata", 1
            except Exception as err:
                print(str(err))
                return str(err), 0

    #################################
    ##  Indirizzi
    #################################
    def addIndirizzo(self, librocard, nomecognome, indirizzo, citta, provincia, paese, numtel, cap ):
        '''Dato Librocard e parametri aggiunge l'indirizzo nel database'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO indirizzi (librocard, nomecognome, indirizzo, citta, provincia, paese, numtel, cap) VALUES( %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ) RETURNING idindirizzo",(librocard, nomecognome, indirizzo, citta, provincia, paese, numtel, cap ))
                idindirizzo = list(cur)
                if idindirizzo:
                    return "Indirizzo salvato", 1 ,idindirizzo[0]
                else:
                    return "Indirizzo non salvato", 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def  getIndirizzo(self, idindirizzo):
        '''Dato idindirizzo ne restituisce i dettagli'''
        #TODO aggiungere controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM indirizzi WHERE idindirizzo = %s",(idindirizzo,))
                indirizzo = list(cur)
                if indirizzo:
                    return "Indirizzo trovato.", 1 ,indirizzo[0]
                else:
                    return "Indirizzo non trovato", 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    def modIndirizzo(self, idindirizzo, nomecognome, indirizzo, citta, provincia, paese, numtel, cap ):
        '''Dato idindirizzo e parametri modifica l'indirizzo nel database'''
        #TODO aggiungere controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("UPDATE indirizzi SET nomecognome = %s, indirizzo = %s, citta = %s, provincia = %s, paese = %s, numtel = %s, cap = %s WHERE idindirizzo  = %s",( nomecognome, indirizzo, citta, provincia, paese, numtel, cap, idindirizzo ))
                return "Indirizzo modificato con successo", 1
            except Exception as err:
                print(str(err))
                return str(err), 0
    
    def eliminaIndirizzo(self, idindirizzo):
        '''Dato idindirizzo elimina l'indirizzo dal database'''
        #TODO aggiungere controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("DELETE FROM indirizzi WHERE idindirizzo  = %s",( idindirizzo, ))
                return "Indirizzo eliminato.", 1
            except Exception as err:
                print(str(err))
                return str(err), 0

    def getIndirizzi(self, librocard):
        '''Dato Librocard e parametri aggiunge l'indirizzo nel database'''
        #TODO aggiungere controlli
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM indirizzi WHERE librocard = %s",(librocard,))
                listindirizzi = list(cur)
                if listindirizzi:
                    return "Indirizzi trovati.", 1 ,listindirizzi
                else:
                    return "Indirizzi non trovati", 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None
