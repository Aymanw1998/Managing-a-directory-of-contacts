#############################################################
# student mail:                                             #
#               1) aymanalwahbani@se.shenkar.ac.il          #
#               2) aebayw@gmail.com                         #
#                                                           #
# Student1 Name: Ayman Wahbani      Student1 Id: 209138155  #
# Student2 Name: Rozeen Hillo       Student2 Id: 205993389  #
#############################################################
#################################################################################
# explanation:                                                                  #
#            input:  number 1 to 4                                              #
#               1 - for add new contact                                         #
#                   input (firstname, lastname, telephone (start - "05")        #
#               2 - for get a list for all contacts from the database(folder)   #
#               3 - for get list for specific contact from the database (folder)#
#                   input (firstname, lastname, telephone (start - "05")        #
#               4 - exit                                                        #
#            output:                                                            #
#               1 - output "Success: Add contact" if all stuff is correct       #
#                      or throw exception                                       #
#               2 - output => print all the contacts or throw exception         #
#               3 - output => print the specific contact                        #
#                   or "Error: Contact doesn't exist"                           #
#            raise:  we have 6 msg for the exception                            #
#################################################################################

import json, os, pandas as pd


# Class Contact
class Contact:
    # Create New Contact (have firstname, lastname, and telephone)
    def __init__(self, firstname: str, lastname: str, telephone: str):
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.telephone: str = telephone


# Class AddressBookException inherits from class Exception
# this is outer class and it has inner classes
class AddressBookException(Exception):
    def __init__(self, commond):
        # if the database or thr folder cannot create
        if commond == "CreateAddressBook":
            self._msg = "Error: The Database cannot create"
        # if the database or the folder is empty
        elif commond == "Empty":
            self._msg = "the database is empty"
        # if the contact/file cannot create
        elif commond == "CreateContact":
            self._msg = "Error: Contact can't create"
        # if we want create new contact/file and there is contact has same telephone
        elif commond == "FoundContact":
            self._msg = "Error: Contact does exist"
        # if we search about file/contact and it doesn't exist
        elif commond == "NotFoundContact":
            self._msg = "Error: Contact doesn't exist"
        # if the file/contact does exist but it isn't opened
        elif commond == "OpenContact":
            self._msg = "Error: can't open the contact file"

    def __str__(self):
        return self._msg


# Class AddressBook
# this is the database or Create database and runs it
class AddressBook:
    # create the database if doesn't exist (Gets the folder/database name)
    def __init__(self, foldername):
        # Checks if the file exists if yes return 1 if no return 0
        if os.listdir().count(foldername) != 0:
            # if yes the file exists, so saves the pathname in field and outgoing
            self.folder = os.path.abspath(foldername)
            return

        try:  # if the file doesn't exist so it tries to create the desired folder/database
            # and saves the pathname in field
            os.mkdir(foldername)
            self.folder = os.path.abspath(foldername)
        except FileExistsError:  # if it was unable to create the folder/database
            # then throw an error AddressBookException
            raise AddressBookException("CreateAddressBook")
        return

    # add the contact to the database, gets contact)
    #   1. create data format json
    #   2. create file
    #   3. add the data on file
    def add_contact(self, contact: Contact):
        # create data format json from the contact
        data = json.dumps({
            'firstname': contact.firstname,
            'lastname': contact.lastname,
            'telephone': contact.telephone
        })
        # linker between folder path and new file name
        # for create new path about new json file location
        path = os.path.join(self.folder, f'{contact.telephone}.json')
        # if the path exists so throw Exception and and don't create an existing file
        if os.path.isfile(path):
            raise AddressBookException("FoundContact")
        try:  # if the path is new so create new file on this path and give it the data
            file = open(path, 'x')
            file.write(data)
        except IOError:  # if there was a fault in the middle of the production of the file
            # and was not create, so throw an error AddressBookException
            raise AddressBookException("CreateContact")
        finally:  # in the end close the file
            file.close()

    # saves all contacts from the database and return them to the list
    def get_contacts(self):
        listf: list = []
        # [file for file in os.listdir(self.folder) if file.endswith('.json')]
        #   takes all json type files from the folder
        # file_name: each time it save the file name in one order after another
        for file_name in [file for file in os.listdir(self.folder) if file.endswith('.json')]:
            # create new path, this path is path of file.json
            path = os.path.join(self.folder, file_name)
            try:  # trying to open the file
                with open(path) as json_file:
                    # takes the information/data from the file about the contact
                    data = json.load(json_file)
                    # insert a list to the desired list each time
                    listf += [data]
            except IOError:  # if the file doesn't open
                # so throw an error AddressBookException
                raise AddressBookException("OpenContact")
            finally:
                json_file.close()
        if not list:
            raise AddressBookException("Empty")
        return listf

    # search about specific contact
    def find_contact(self, firstname: str, lastname: str, telephone: int):
        # takes the name file with have correct name: {telephone}.json
        res = [file for file in os.listdir(self.folder) if file.endswith(f'{telephone}.json')]
        # if res(the list) has the name file so has contact so goes into the loop
        for item in res:
            path = os.path.join(self.folder, item)
            try:
                file = open(path, 'r')
                data = json.load(file)
                if data["firstname"] == firstname and data["lastname"] == lastname and data["telephone"] == telephone:
                    # return list that has path and data
                    file.close()
                    return [data]
            except IOError:
                raise AddressBookException("OpenContact")
        raise AddressBookException("NotFoundContact")


def main():
    try: # Create the database/folder if is not exist
        addressBook: AddressBook = AddressBook("AddressBook")
    except AddressBookException as e:
        print(e + ", so we cannot continue")
        return
    firstName: str = None
    lastName: str = None
    telephone: str = None

    # loop for we want the user choose the options more then one
    while 1:
        print("""
            ------ DataBase name is AddressBook ------
            1. Add New Contact
            2. Print Contacts from AddressBook
            3. found specific contact
            4. Exit
            """)
        # i : is the number for option
        i = input("choose 1 to 4: ")
        if i == "1" or i == "3":
            # create object contact
            firstName = input("Enter FistName: ")
            lastName = input("Enter LastName: ")
            telephone = "0"
            while len(telephone) != 10 or telephone[0:2] != "05":
                telephone = input("Enter telephone: ")
                if len(telephone) != 10 or telephone[0:2] != "05":
                    print("Error number. Enter again please (10 number, start 05)")
            contact = Contact(firstName, lastName, telephone)
            if i == "1":
                try:
                    addressBook.add_contact(contact)
                    print("Success: Add contact")
                except AddressBookException as ex:
                    print(ex)
            elif i == "3":
                try:
                    find_contact = addressBook.find_contact(firstName, lastName, telephone)
                    print("Print thr specific contact from AddressBook")
                    print("the data is exist in file: => {} ".format(find_contact[0]))
                except AddressBookException as ex:
                    print(ex)
        elif i == "2":
            try:
                getcontacts = addressBook.get_contacts()
                count: int = 0
                print("Print all contacts from AddressBook\n")
                for i in getcontacts:
                    count = count + 1
                    print("Contact %d : %s" % (count, i))
            except AddressBookException as ex:
                print(ex)
        elif i == "4":
            return
        else:
            print("Error: Enter just 1, 2, 3, or 4. ")


if __name__ == "__main__":
    main()
