import sqlite3 as sql
import inCollege

#connects to the database file that was created
sqlfile = "database.sqlite"
source = sql.connect(sqlfile)
cursor = source.cursor()

#main Function
def Main():

        inCollege.successStory()
        print("Would you like to sign in or sign up? 0 for sign in, and 1 for sign up: ")
        print("3 for information video | Search Person 4")
        print("5 for Useful Links | 6 for InCollege Important Links")
        option = input()

        while option != "1" and option != "0" and option != "3" and option != "4" and option != "5" and option != "6":
            option = input("Incorrect input. 0 for sign in, 1 for sign up, 3 for more information, search 4, useful links 5, InCollege links 6: ")
        
        if option == "0":
            status, username = inCollege.logIn(cursor)
        elif option == "1":
            status, username = inCollege.signUp(cursor,source)
        elif option == "3":
            status = inCollege.PlayVideo()
        elif option == "4":
            status = inCollege.FindPerson(cursor)
        elif option == "5":
            status = inCollege.UsefulLink(cursor)
        elif option == "6":
            status = inCollege.InCollegeLink(cursor)


        if status:
            print("Logged in!")
            # use user to bounce around the functions as needed
            user = inCollege.Options(cursor, source, username)

        source.close()
if __name__ == "__main__":
    Main()