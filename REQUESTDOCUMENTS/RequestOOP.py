

class Request:
    def __init__(self,document_id,  typeOfCertificate, residentID, price, official_id):
        self.__document_id = document_id
        self.__typeOfCertificate = typeOfCertificate
        self.__resident = residentID
        self.__price = price
        self.__official_id = official_id


    @property
    def document_id(self):
        return self.__document_id

    @property
    def typeOfCertificate(self):
        return self.__typeOfCertificate
    @property
    def residentID(self):
        return self.__resident

    @property
    def Price(self):
        return self.__price

    @property
    def official_id(self):
        return self.__official_id


    @document_id.setter
    def document_id(self, document_id):
        self.__document_id = document_id
    @typeOfCertificate.setter
    def typeOfCertificate(self, typeOfCertificate):
           self.__typeOfCertificate = typeOfCertificate

    @residentID.setter
    def residentID(self, residentID):
        self.__resident = residentID

    @Price.setter
    def Price(self, price):
        self.__price = price

    @official_id.setter
    def official_id(self, official_id):
        self.__official_id = official_id

