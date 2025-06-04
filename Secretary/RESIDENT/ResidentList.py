class ResidentList:
    def __init__(self, firstname, lastname, middlename, dob, pob, nationality,
                 religion, purok, gender, pwd, deceased, bloodtype, height, father, mother):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__middlename = middlename
        self.__dob = dob
        self.__pob = pob
        self.__nationality = nationality
        self.__religion = religion
        self.__purok = purok
        self.__gender = gender
        self.__pwd = pwd
        self.__deceased = deceased
        self.__bloodtype = bloodtype
        self.__height = height
        self.__father = father
        self.__mother = mother

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, value):
        self.__firstname = value

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, value):
        self.__lastname = value

    @property
    def middlename(self):
        return self.__middlename

    @middlename.setter
    def middlename(self, value):
        self.__middlename = value

    @property
    def dob(self):
        return self.__dob

    @dob.setter
    def dob(self, value):
        self.__dob = value

    @property
    def pob(self):
        return self.__pob

    @pob.setter
    def pob(self, value):
        self.__pob = value

    @property
    def nationality(self):
        return self.__nationality

    @nationality.setter
    def nationality(self, value):
        self.__nationality = value

    @property
    def religion(self):
        return self.__religion

    @religion.setter
    def religion(self, value):
        self.__religion = value

    @property
    def purok(self):
        return self.__purok

    @purok.setter
    def purok(self, value):
        self.__purok = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @property
    def pwd(self):
        return self.__pwd

    @pwd.setter
    def pwd(self, value):
        self.__pwd = value

    @property
    def deceased(self):
        return self.__deceased

    @deceased.setter
    def deceased(self, value):
        self.__deceased = value

    @property
    def bloodtype(self):
        return self.__bloodtype

    @bloodtype.setter
    def bloodtype(self, value):
        self.__bloodtype = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def father(self):
        return self.__father

    @father.setter
    def father(self, value):
        self.__father = value

    @property
    def mother(self):
        return self.__mother

    @mother.setter
    def mother(self, value):
        self.__mother = value
