#!/usr/bin/env python3

import sys
import os
import subprocess
import gzip


class IDMappingUniRefChopper:

    def __init__(self):
        # Original (unedited) idmapping file to be searched
        self.idmapping_file = None
        # Original (unedited) uniref file to be searched
        self.uniref_file = None
        # idmapping file edited by desired database
        self.idmapping_file_by_database = None
        # idmapping file edited by desired UniRef numbers
        self.idmapping_file_by_uniref = None
        # idmapping file edited by uniref entries corresponding with desired database
        self.idmapping_file_by_database_and_uniref = None
        # Unique idmapping file edited by uniref entries corresponding with desired database
        self.idmapping_file_by_database_and_uniref_unique = None

        # Menu Option:
        self.option0 = " 0. Exit."
        self.option1 = " 1. Create new idmapping file filtered by desired database name (e.g. PATRIC, UniRef90)."
        self.option2 = " 2. Create new idmapping file filtered by UniRef entries with corresponding database name."
        self.option3 = " 3. Create new UniRef file filtered by entries with corresponding desired database name."
        self.option4 = " 4. Steps 1 - 3."

    # Displays menu options for user:
    def display_options(self):
        print("\n\n | MAIN MENU |")
        print(" -------------")
        print(self.option0)
        print(self.option1)
        print(self.option2)
        print(self.option3)
        print(self.option4)
        #print(" 4. All of the above.")
        selection = int(input("Please enter the number corresponding to your selection: "))
        return selection

    # Returns file if file is to be used; returns None if file is not to be used.
    def checkForExistingFile(self, file):
        # If record of file exists:
        if not file is None:
            valid_answer = False
            while not valid_answer:
                answer = input("\nUse file %s? [y/n] " % file)
                if answer is "y":
                    valid_answer = True
                    return file
                elif answer is "n":
                    valid_answer = True
                    return None
                else:
                    valid_answer = False
                    "Invalid entry."
        else:
            return None

    def promptUserForFile(self):
        file = input("File: ")
        # This will return a valid file or None if user opted to return:
        return self.checkThatFileIsValid(file)

    def checkThatFileIsValid(self, file):
        # Check that user-specified file is valid:
        while not os.path.exists(file):
            temp = input("\nInvalid file or path. Please try again, or enter 0 to return: ")
            if temp is "0":
                return None
            else:
                file = temp
        return file

    def checkForMistakenSelection(self):
        answer = input("If this is a mistake, please enter 0 to return to the main menu. To continue, press enter: ")
        if answer is "0":
            return 0

    def enterIdmappingFile(self):
        # Prompt user for idmapping file to be searched:
        print("Enter idmapping file to be searched (e.g. idmapping.dat.gz): ")
        idmapping_file = self.promptUserForFile()

        # Method promptUserForFile will ensure file is valid or return None
        if idmapping_file is None:
            return 0
        else:
            self.idmapping_file = idmapping_file
            return 1

    def selection1work(self, database, idmapping_file, db_filtered_file):
        # Looking for specified database in the original idmapping file
        print("\nLooking for entries of " + database + " in " + idmapping_file)
        subprocess.call('zgrep {} {} > {}'.format(database, idmapping_file, db_filtered_file), shell=True)
        print("\nCompleted search for " + database + " in " + idmapping_file + ". Results in " + db_filtered_file)

        if "UniRef" in database:
            self.idmapping_file_by_uniref = db_filtered_file
        else:
            self.idmapping_file_by_database = db_filtered_file

    def selection1(self):
        # Double-check that user selected the correct option. If not, return to main menu.
        print("\nYou selected: " + self.option1)
        if self.checkForMistakenSelection() is 0:
            return 0

        # Check if self.idmapping_file has already been entered and if the user wants to use this file.
        # Returns None if the file has not been entered, or if the user does not want to use it.
        # Otherwise, returns the file.
        if self.checkForExistingFile(self.idmapping_file) is None:
            if self.enterIdmappingFile() is 0:
                return 0

        # Prompt user for desired database name:
        database = input("\nEnter name of database to look for (e.g. PATRIC, UniRef90). \n"
                             "NOTE: This entry is case-sensitive!: ")

        db_filtered_file = database + "_" + self.idmapping_file

        self.selection1work(database, self.idmapping_file, db_filtered_file)

        return 1

    def __enterIdmappingFileByDatabase(self, identifier):
        if identifier is "database":
            print("\nEnter idmapping file filtered by desired database \n"
                  "(e.g. PATRIC_idmapping.dat.gz): ")
        else:
            print("\nEnter idmapping file filtered by desired database \n"
                  "(e.g. UniRef90_idmapping.dat.gz): ")
        file = self.promptUserForFile()

        # Method promptUserForFile will ensure file is valid or return None
        if file is None:
            return 0
        else:
            if identifier is "database":
                self.idmapping_file_by_database = file
            else:
                self.idmapping_file_by_uniref = file

            return 1

    def __selection2SubRoutine_CheckForIdmappingFileByDatabase(self, file, identifier):
        # Check if self.idmapping_file_by_database or self.idmapping_file_by_uniref
        # already exists and if the user wants to use this file.
        # Returns None if the file has not been entered, or if the user does not want to use it.
        # Otherwise, returns the file.
        if self.checkForExistingFile(file) is None:
            ######## The above could return None if file has not been entered or entered file is not to be used
            valid_answer = False
            while not valid_answer:
                if identifier is "database":
                    answer = input("\nDo you want to use an existing idmapping file filtered by desired database \n"
                                       "(e.g. PATRIC_idmapping.dat.gz)? [y/n] ")
                else:
                    answer = input("\nDo you want to use an existing idmapping file filtered by desired database \n"
                                       "(e.g UniRef90_idmapping.dat.gz)? [y/n] ")
                # If answer is yes, prompt user to enter the file:
                if answer is "y":
                    if self.__enterIdmappingFileByDatabase(identifier) is 0:
                        valid_answer = False
                    else:
                        valid_answer = True
                        return 1
                # If answer is no, the file will have to be created:
                elif answer is "n":
                    valid_answer = True
                    # Check if self.idmapping_file already exists and if the user wants to use this file.
                    # Returns None if the file has not been entered, or if the user does not want to use it.
                    # Otherwise, returns the file.
                    if self.checkForExistingFile(self.idmapping_file) is None:
                        if self.enterIdmappingFile() is 0:
                            return 0
                    # If we have reached this point, we should have a valid, usable self.idmapping_file!
                    # Prompt user for desired database name:
                    database = input("\nEnter name of database to look for (e.g. PATRIC). \n"
                                         "NOTE: This entry is case-sensitive!: ")

                    db_filtered_file = database + "_" + self.idmapping_file

                    self.selection1work(database, self.idmapping_file, db_filtered_file)
                    # If we have reached this point, we should have a valid, usable
                    # self.idmapping_file_by_database or self.idmapping_file_by_uniref!
                    return 1
                else:
                    valid_answer = False
                    print("Invalid entry.")
        return 1

    def selection2work(self):

        db_filtered_file = self.idmapping_file_by_database
        uniref_filtered_file = self.idmapping_file_by_uniref
        uniref_with_database_file = "UniRef_" + self.idmapping_file_by_database
        unique_uniref_with_database_file = "Unique_" + uniref_with_database_file

        # Looking for specified database entries with a UniRef90 entry
        print("\nLooking for UniRef entries in " + uniref_filtered_file +
              " with corresponding entries in " + db_filtered_file)
        subprocess.call('./dblookup.sh {} {} {} {}'.format(db_filtered_file, uniref_filtered_file,
                                                            uniref_with_database_file,
                                                            unique_uniref_with_database_file), shell=True)
        print("\nCompleted search for UniRef entries in " + uniref_filtered_file + " with corresponding entries in "
              + db_filtered_file + ". Results in " + uniref_with_database_file)
        print("\nUnique results in " + unique_uniref_with_database_file)

        self.idmapping_file_by_database_and_uniref = uniref_with_database_file
        self.idmapping_file_by_database_and_uniref_unique = unique_uniref_with_database_file

    def selection2(self):
        # Double-check that user selected the correct option. If not, return to main menu.
        print("\nYou selected: " + self.option2)
        if self.checkForMistakenSelection() is 0:
            return 0

        print("\n----------")
        print("This selection requires an idmapping file filtered by desired database \n"
              "(e.g. PATRIC_idmapping.dat.gz).")
        if self.__selection2SubRoutine_CheckForIdmappingFileByDatabase(self.idmapping_file_by_database, "database") is 0:
            return 0

        print("\n----------")
        print("This selection requires an idmapping file filtered by desired database \n"
              "(e.g. UniRef90_idmapping.dat.gz).")
        if self.__selection2SubRoutine_CheckForIdmappingFileByDatabase(self.idmapping_file_by_uniref, "UniRef") is 0:
            return 0

        self.selection2work()

        return 1

    def __enterIdmappingFileByDatabaseAndUnirefUnique(self):
        print("\nEnter idmapping file containing unique UniRef entries associated \n"
                "with a desired database (e.g. Unique_UniRef_PATRIC_idmapping.dat.gz): ")
        file = self.promptUserForFile()

        # Method promptUserForFile will ensure file is valid or return None
        if file is None:
            return 0
        else:
            self.idmapping_file_by_database_and_uniref_unique = file
            return 1

    def __selection3subroutine_CheckForIdmappingFileByDatabaseAndUnirefUnique(self, file):
        # Check if self.idmapping_file_by_database_and_uniref_unique already exists and if the user wants to use this file.
        # Returns None if the file has not been entered, or if the user does not want to use it.
        # Otherwise, returns the file.
        if self.checkForExistingFile(file) is None:
            valid_answer = False
            while not valid_answer:
                answer = input("Do you want to use an existing idmapping file containing unique UniRef entries \n"
                                   "associated with a desired database (e.g. Unique_UniRef_PATRIC_idmapping.dat.gz)? [y/n] ")
                # If answer is yes, prompt user to enter the file:
                if answer is "y":
                    valid_answer = True
                    if self.__enterIdmappingFileByDatabaseAndUnirefUnique() is 0:
                        valid_answer = False
                    else:
                        valid_answer = True
                        return 1
                # If answer is no, the file will have to be created:
                elif answer is "n":
                    valid_answer = True
                    print("\n----------")
                    print("This selection requires an idmapping file filtered by desired database \n"
                          "(e.g. PATRIC_idmapping.dat.gz).")
                    if self.__selection2SubRoutine_CheckForIdmappingFileByDatabase(
                            self.idmapping_file_by_database, "database") is 0:
                        return 0

                    print("----------")
                    print("\nThis selection requires an idmapping file filtered by desired database \n"
                          "(e.g. UniRef90_idmapping.dat.gz).")
                    if self.__selection2SubRoutine_CheckForIdmappingFileByDatabase(
                            self.idmapping_file_by_uniref, "UniRef") is 0:
                        return 0

                    self.selection2work()
                    return 1
                else:
                    valid_answer = False
                    print("Invalid entry.")
        return 1

    def enterUnirefFile(self):
        # Prompt user for uniref file to be searched:
        print("Enter UniRef file to be searched (e.g. uniref90.fasta.gz): ")
        uniref_file = self.promptUserForFile()

        # Method promptUserForFile will ensure file is valid or return None
        if uniref_file is None:
            return 0
        else:
            self.uniref_file = uniref_file
            return 1

    def selection3work(self):

        print("\nLooking for UniRef entries in " + self.uniref_file +
              " with corresponding entries in " + self.idmapping_file_by_database_and_uniref_unique)

        # Creating set of all the cross-reference id's
        # unique_uniref_set to contain all UniRefIDs corresponding to desired databases
        unique_uniref_set = set()
        with open(self.idmapping_file_by_database_and_uniref_unique, 'r') as file_to_read:
            for line in file_to_read:
                unique_uniref_set.add(">" + line.strip("\n"))

        file_to_write = open("UniRef_Chopped_By_Database.fasta.gz", "w")
        with gzip.open(self.uniref_file, 'r') as uniref_file:
            write = False
            for line in uniref_file:
                if b">" in line:
                    dline = line.decode("utf-8")
                    if dline.split(" ")[0] in unique_uniref_set:
                        write = True
                    else:
                        write = False
                if write:
                    file_to_write.write(line.decode("utf-8"))

        print("\nCompleted search for UniRef entries in " + self.uniref_file + " with corresponding entries in "
              + self.idmapping_file_by_database_and_uniref_unique + ". Results in UniRef_Chopped_By_Database.fasta.gz.")

    def selection3(self):
        # Double-check that user selected the correct option. If not, return to main menu.
        print("\nYou selected: " + self.option3)
        if self.checkForMistakenSelection() is 0:
            return 0

        print("\n----------")
        print("This selection requires an idmapping file containing unique UniRef entries associated with \n"
              "a desired database (e.g. Unique_UniRef_PATRIC_idmapping.dat.gz).")
        if self.__selection3subroutine_CheckForIdmappingFileByDatabaseAndUnirefUnique(
            self.idmapping_file_by_database_and_uniref_unique) is 0:
            return 0

        if self.checkForExistingFile(self.uniref_file) is None:
            if self.enterUnirefFile() is 0:
                return 0

        self.selection3work()

        return 1

    def selection4(self):
        # Double-check that user selected the correct option. If not, return to main menu.
        print("\nYou selected: " + self.option4)
        if self.checkForMistakenSelection() is 0:
            return 0

        print("\n----------")
        # If this function returns 0, there is some sort of problem. Return.
        # If not, self.idmapping_file has been set.
        if self.enterIdmappingFile() is 0:
            return 0

        print("\n----------")
        # Prompt user for desired database name:
        database = input("Enter name of database to look for (e.g. PATRIC). \n"
                             "NOTE: This entry is case-sensitive!: ")

        print("\n----------")
        # Prompt user for desired database name:
        uniref_database = input("Enter name of database to look for (e.g. UniRef90). \n"
                             "NOTE: This entry is case-sensitive!: ")

        print("\n----------")
        # If this function returns 0, there is some sort of problem. Return.
        # If not, self.uniref_file has been set.
        if self.enterUnirefFile() is 0:
            return 0

        print("\n----------------------------------------")
        print("Sit back and relax. This may take a while... ")
        print("----------------------------------------")

        # This will create self.idmapping_file_by_database
        db_filtered_file = database + "_" + self.idmapping_file
        self.selection1work(database, self.idmapping_file, db_filtered_file)

        # This will create self.idmapping_file_by_uniref
        uniref_filtered_file = uniref_database + "_" + self.idmapping_file
        self.selection1work(uniref_database, self.idmapping_file, uniref_filtered_file)

        # This will create self.idmapping_file_by_database_and_uniref
        # This will create self.idmapping_file_by_database_and_uniref_unique
        self.selection2work()

        self.selection3work()

        return 1

    def run(self):
        exit_boolean = False
        while not exit_boolean:
            selection = self.display_options()

            if selection is 0:
                exit_boolean = True
            elif selection is 1:
                if self.selection1() is 0:
                    print("\nSelection 1 did not complete. Please try again, or choose a different option.")
                else:
                    print("\nSelection 1 complete!")
            elif selection is 2:
                if self.selection2() is 0:
                    print("\nSelection 2 did not complete. Please try again, or choose a different option.")
                else:
                    print("\nSelection 2 complete!")
            elif selection is 3:
                if self.selection3() is 0:
                    print("\nSelection 3 did not complete. Please try again, or choose a different option.")
                else:
                    print("\nSelection 3 complete!")
            elif selection is 4:
                if self.selection4() is 0:
                    print("\nSelection 4 did not complete. Please try again, or choose a different option.")
                else:
                    print("\nSelection 4 complete!")


chopper = IDMappingUniRefChopper()
chopper.run()
