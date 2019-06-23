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
                return "Autore inserito.", 1 , idedit #ritorno la casa editrice
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
                cur.execute("SELECT * FROM generi")
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


    #################################
    ##  Query getLibro (model present)
    #################################
    def getLibro(self, isbn):
        '''Fetcha il libro con isbn se presente, ritorna errore altrimenti'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM libri JOIN autori ON libri.idaut = autori.idaut JOIN case_editrici ON libri.idedit = case_editrici.idedit WHERE isbn=%s ", (str(isbn),))
                libro = list(cur)[0]
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
    ##  login (model present)
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
    ##  carrello
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
    ##  addCart
    #################################
    def addCart(self,idord, isbn, quant):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO rel_ord_lib(idord,isbn,rel_quant) VALUES (%s,%s,%s)", (idord, isbn, quant))
                return "Libro inserito nel carrello", 1 
            except psycopg2.IntegrityError:
                return "Libro giá presente nel carrello", 0
            except Exception as err:
                print(str(err))
                return str(err), 0
    #################################
    ##  gestione ordine
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
                    return "Libri nell'ordine trovati", 1 ,libri
                else:
                    return "Libri nell'ordine %s non trovati"%(idord), 0 ,None
            except Exception as err:
                print(str(err))
                return str(err), 0, None