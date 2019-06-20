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
    ##  Query
    #################################

    #################################
    ##  Registrazione
    #################################
    def registrazione(self, nome, cognome, mail, password):
        with type( self ).__cursor() as cur:
            try:
                print("INSERT INTO utenti (Nome, Cognome, Mail, Password, DataReg) VALUES(%s, %s, %s, %s, NOW())" %(nome, cognome, mail, password))
                cur.execute("INSERT INTO utenti (Nome, Cognome, Mail, Password, DataReg) VALUES(%s, %s, %s, %s, NOW())", (nome,cognome, mail, password))
                return 1, "Utente Registrato!" 
            except psycopg2.IntegrityError as err:
                print(err.__str__)
                return 0, "Email già inserita"
            except Exception as err:
                print(str(err))
                return 0, str(err)