import psycopg2.extras
from configparser import ConfigParser
#import configparser

class DM_postgre():
    __server = __db = __db4Log = __user = __password = __dbCon =__db4LogCon =__nIstanze = None

    # def __init__(self):    


    @classmethod
    def __open(cls):
        Config = ConfigParser()
        Config.read("server.ini")
        # print(Config["server"]["server"])
        cls.__server = Config["server"]["server"]
        cls.__db =Config["server"]["db"]
        cls.__db4Log = Config["server"]["db4log"]
        cls.__user = Config["server"]["user"]
        cls.__password = Config["server"]["password"]
        cls.__dbCon = None # La connessione è condivisa !
        cls.__db4LogCon = None # La connessione è condivisa !
        cls.__nIstanze = 0
        if cls.__dbCon is None :
            try :
                cls.__dbCon = psycopg2.connect( host = cls.__server, database = cls.__db , user = cls.__user , password = cls.__password )
                cls.__dbCon.set_session( readonly = False, autocommit = True ) # Connessione di lettura condivisa, connect_timeout = 3
                print("|-- Connection to database " + cls.__db + " created .")
                print(cls.__dbCon)
            except psycopg2.OperationalError as err:
                print("|-- 1) Error connecting to PostgreSQL DBMS at %s. nDetails : %s." %( cls.__server , err))
                cls.__dbCon = cls.__db4LogCon = None
                exit()
            # else : # Questo else è del TRY
            #     try :
            #         cls.__db4LogCon = psycopg2.connect( host = cls.__server , database = cls.__db4Log, user = cls.__user , password = cls.__password )
            #         cls.__db4LogCon.set_session( autocommit = True ) #Connessione di scrittura condivisa
            #         #print(" Connection to database " + cls.__db4LogCon + " created .")
            #     except psycop2.OperationalError as err:
            #         print(" 2) Error connecting to PostgreSQL DBMS at %s. nDetails : %s."%( cls.__server , err))
            #         cls.__dbCon = cls.__db4LogCon = None
            #         exit()
            print("|-- New connection opened .")
            return " New connection opened ."
        print(" Connection already opened .")
        return "|-- Connection already opened ."

    @classmethod
    def __close(cls):
        if cls.__nIstanze == 0 and cls.__dbCon is not None :
            cls.__dbCon.close()
            # cls.__db4LogCon.close()
            print("-- Connection closed .")
            cls.__dbCon = cls.__db4LogCon = None

    @classmethod
    def __cursor(cls):
        """ Ritorna un cursore che restituisce dict invece di tuple per ciascuna riga di una select ."""
        print('|-- Richiesta cursore da:')
        print(cls.__dbCon)
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

    def getlistacose(self):
        with type( self ).__cursor() as cur:
            cur.execute("SELECT * FROM tabella1")
            lista=list(cur)
            return lista
    
    def elimina(self, id):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("DELETE FROM tabella1 where idn = %s"%(id))
                return str(id)+" eliminato!"
            except psycopg2.Error as err:
                print(err.__str__)
                return str(err)

    def insertcose(self, nome, quant):
        with type( self ).__cursor() as cur:
            try:
                cur.execute("INSERT INTO tabella1(nome, quant) VALUES(%s, %s)",(nome,quant))
                return "Oggetto inserito!" 
            except psycopg2.Error as err:
                print(err.__str__)
                return str(err)




    


        