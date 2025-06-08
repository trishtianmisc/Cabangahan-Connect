
class ResidentComp:
    def __init__(self, complaint_id ,complainant, residentID, typeOfComplaint, date, details, official_id, status='pending'):
        self.__complaint_id = complaint_id
        self.__complainant = complainant
        self.__residentID = residentID
        self.__typeOfComplaint = typeOfComplaint
        self.__date = date
        self.__details = details
        self.__status = status
        self.__official_id = official_id

    @property
    def complaint_id(self):
        return self.__complaint_id

    @property
    def complainant(self):
        return self.__complainant

    @property
    def residentID(self):
        return self.__residentID

    @property
    def typeOfComplaint(self):
        return self.__typeOfComplaint

    @property
    def date(self):
        return self.__date

    @property
    def details(self):
        return self.__details

    @property
    def status(self):
        return self.__status

    @property
    def official_id(self):
        return self.__official_id

    @complaint_id.setter
    def complaint_id(self, complaint_id):
        self.__complaint_id = complaint_id

    @complainant.setter
    def complainant(self, complainant):
        self.__complainant = complainant

    @residentID.setter
    def residentID(self, residentID):
        self.__residentID = residentID

    @typeOfComplaint.setter
    def typeOfComplaint(self, typeOfComplaint):
        self.__typeOfComplaint = typeOfComplaint

    @date.setter
    def date(self, date):
        self.__date = date

    @details.setter
    def details(self, details):
        self.__details = details



    @status.setter
    def status(self, value):
        if value in ["pending", "solved"]:
            self.__status = value
        else:
            raise ValueError("Invalid status")

    @official_id.setter
    def official_id(self, official_id):
        self.__official_id = official_id
