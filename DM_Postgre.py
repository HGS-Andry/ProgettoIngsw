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
    def addAutore(self, nome):
        '''Registra l'autore nuovo. Ritorna messaggio e result (0 errore, 1 effettuato) e idaut'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO autori (nome) values(%s) RETURNING idaut", (nome))
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
                return "Editrici Fetchate", 1 , list(cur) #ritorno la casa editrice
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    #################################
    ##  Query AddEdit (model present)
    #################################
    def addEdit(self, nome):
        '''Registra la casa editrice nuova. Ritorna messaggio e result (0 errore, 1 effettuato) e idEdit'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO casa_editrice (nome) values(%s) RETURNING idedit", (nome))
                return "Autore inserito.", 1 , idedit #ritorno la casa editrice
            except Exception as err:
                print(str(err))
                return str(err), 0, None
    

    #################################
    ##  Query getLibro
    #################################
    def getLibro(self, isbn):
        '''Fetcha il libro con isbn se presente, ritorna errore altrimenti'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("SELECT * FROM libri WHERE isbn='%s'", (isbn))
                libro = list(cur)[0]
                if libro:
                    return "Libro Fetchato", 1 , list(cur)[0] #ritorno la casa editrice
                else:
                    return ("Il libro con ISBN %s non è presente nel Database" % isbn)
            except Exception as err:
                print(str(err))
                return str(err), 0, None

    #################################
    ##  Query addLibri (model present)
    #################################
    def addLibro(self, isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant):
        '''Registra l'utente nuovo. Ritorna messaggio e result (0 errore, 1 effettuato) e librocard'''
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO libri (isbn, titolo, datapubb, prezzo, punti, descr, posclas, immagine , idEdit, quant) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (isbn, titolo, datapubb, prezzo, punti, descr, posclas, dataAggClas, immagine , idEdit, quant))
                return "Libro inserito.", 1, isbn #ritorno l'isbn
            except Exception as err:
                print(str(err))
                return str(err), 0, None

                
    #################################
    ##  Registrazione (model present)
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
    ##  Login (model present)
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