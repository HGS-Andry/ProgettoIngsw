from datetime import date , datetime
from DM_Postgre import DM_postgre

class Model(object):
    def __init__(self):
        self.id = " Model_ " + date.today().isoformat()
        print("|- creato model")
        self.dataMapper = DM_postgre()   

    def insertcose(self, nom, quant):
        #controllo input
        # try:
        code = self.dataMapper.insertcose(nom, quant)
        print(code)
        return code 
        # except:
        #     return "C'è stato un errore!"

    def getlistacose(self):
        print("|- getlista cose")
        lista = self.dataMapper.getlistacose()
        # for i in lista:
        #     print(i[1])
        return lista

    def close(self):
        print("|- chiudiamo")
        self.dataMapper.close()

    # def __del__ ( self ):
    #     self.__close()
        