class ResidentComp:
    def __init__(self, non_cabangahan_comp_id, non_complainant, non_address, non_place,
                 non_type_of_complainant, complaint_date, details, official_id, status='pending'):
        self.__complaint_id = non_cabangahan_comp_id
        self.__complainant = non_complainant
        self.__address = non_address
        self.__place = non_place
        self.__type_of_complainant = non_type_of_complainant
        self.__date = complaint_date
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
    def address(self):
        return self.__address

    @property
    def place(self):
        return self.__place

    @property
    def type_of_complainant(self):
        return self.__type_of_complainant

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
    def complaint_id(self, value):
        self.__complaint_id = value

    @complainant.setter
    def complainant(self, value):
        self.__complainant = value

    @address.setter
    def address(self, value):
        self.__address = value

    @place.setter
    def place(self, value):
        self.__place = value

    @type_of_complainant.setter
    def type_of_complainant(self, value):
        self.__type_of_complainant = value

    @date.setter
    def date(self, value):
        self.__date = value

    @details.setter
    def details(self, value):
        self.__details = value

    @status.setter
    def status(self, value):
        if value in ["pending", "solved"]:
            self.__status = value
        else:
            raise ValueError("Invalid status. Must be 'pending' or 'solved'.")

    @official_id.setter
    def official_id(self, value):
        self.__official_id = value
