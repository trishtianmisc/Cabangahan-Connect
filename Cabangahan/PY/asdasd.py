from database import Database

def main():
    db = Database()
    residents = db.fetch_residents()

    if not residents:
        print("No residents found.")
        return

    print("Resident List:")
    for res in residents:
        print(f"{res.firstname} {res.middlename} {res.lastname}, "
              f"DOB: {res.dob}, Place of Birth: {res.pob}, "
              f"Nationality: {res.nationality}, Religion: {res.religion}, "
              f"Gender: {res.gender}, Blood Type: {res.bloodtype}, "
              f"Father: {res.father}, Mother: {res.mother}")

def certificate(sself):
    db = Database()
    resident = db.fetch_residents()

    resident 

if __name__ == "__main__":
    main()
