#Antonio Gonzalez, U57195076
#Kevin Girjanand, U68848880
#Jesse Gonzales, U96407722


import time as t
import sqlite3 as sql

def logIn(cursor):
    cont = True
    while cont:
        #asks for username and password and attempts to find it in the database
        username = input("What is your username?: ")
        password = input("What is your password?: ")
        cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))

        #if the query is successful, then it logs in, otherwise, it prints an error statement
        data = cursor.fetchall()
        if len(data) == 0:
            print("user does not exist with this username and password combination")
        else:
            loggedIn = True
            cont = False
    return loggedIn, username

def signUp(cursor,source):
    #first checks if the number of rows in Users is 5, if so, that's the maximum number of users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 5:
        print("Unable to sign up. There is already the maximum number of users.")
        loggedIn = False
        username = " "
    else:
        cont = True
        #asks for the username and then searches the database for that username, printing an error if found
        username = input("What is your desired username?: ")
        while cont:
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            data = cursor.fetchall()
            if len(data) == 0:
                cont = False
            else:
                print("Username already exists")
                username = input("Input a new one: ")
        password = input("What is your desired password?: ")

        cont = True

        #simple input checking for the password
        while cont:
            capital = any(word.isupper() for word in password)
            digit = any(word.isdigit() for word in password)
            if len(password) < 8 or len(password) > 12 or capital == False or digit == False or password.isalnum() == True:
                print("Invalid option. Password must between 8 and 12 characters, have a digit, capital letter, and a special character")
                password = input("Try another password: ")
            else:
                cont = False
                
        cont = True
        
        #Enter first name
        firstName = input("What is your first name?: ")
        lastName = input("What is your last name?: ")
        while cont:
            cursor.execute("SELECT firstName FROM users WHERE firstName = ?", (firstName,))
            fNames = cursor.fetchall()
            if len(fNames) == 0:
                cont = False
            else:
                while cont:
                    cursor.execute("SELECT lastName FROM users WHERE lastName = ?", (lastName,))
                    lNames = cursor.fetchall()
                    if len(lNames) == 0:
                        cont = False
                    else:
                        cursor.execute("SELECT * FROM users")
                        names = cursor.fetchall()
                        names = list(names)
                        for name in names:
                            if(firstName == name[2] and lastName == name[3]):
                                print("User already exists")
                                firstName = input("Please enter another first name: ")
                                lastName = input("Please enter another last name: ")
                            else:
                                continue
                        cont = False
            
        
        cont = True

        #adds inputs into the Users table, thus making a new row
        addVal = """
        INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);"""

        cursor.execute(addVal,(username, password, firstName, lastName))
        source.commit()
        loggedIn = True
    return loggedIn, username

def PlayVideo():
    print("Video is now playing\n")
    #Waits 4 seconds so user can watch the video then present option to join or go to main menu
    t.sleep(4)
    user  = input("Sign up: 0\n")
    if user != "0":
        Main()
    else:
        signUp(cursor, source)
        
def successStory():
    print("Thanks to inCollege I was able to meet with fellow college students and establish connections")
    print("that allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege")
    print("I was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft")
    print("--Alyssa (Arizona)")

# Functions After Logged In
# ====================================================================================================
def Options(username):
    print("Select Option")
    print("============================================================")
    UserOpt = input(
        "Search for a Job | Find Someone | Learn Skill\n============================================================\n")

    UserSelection(UserOpt.lower(), username)

def UserSelection(option, username):
    if option == "search for a job":
        SearchJob(username)
    elif option == "find someone":
        FindPerson(cursor,username)
    elif option == "learn skill":
        SkillSelect(username)
    else:
        "Invalid Selection"
        Options(username)


def SearchJob(username):
    post_job = input("Would you like to post a job?: ")
    
    if(post_job == "yes"):
        print("Posting job now")
        
        cursor.execute("SELECT * FROM users")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if(item[0] == username):
                userFirst = item[2]
                userLast = item[3]
        
        cursor.execute("SELECT COUNT(*) FROM jobs")
        if(cursor.fetchone()[0] == 5):
            print("Unable to add job. There is already the maximum number of jobs posted.")
        else:
            title = input("Enter a job title: ")
            description = input("Enter a job description: ")
            employer = input("Enter name of employer: ")
            location = input("Enter a location: ")
            salary = input("Enter a salary: ")
            
            #adds inputs into the jobs table, thus making a new row
            addJob = """
            INSERT INTO jobs (title, description, employer, location, salary, first, last) VALUES (?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(addJob,(title, description, employer, location, salary, userFirst, userLast))
            source.commit()


            print("To post another job, press 1:")
            user = input()
            if user == "1":
                SearchJob(username)
            else:
                Options(username)
                print("")
    else:       
        Options(username)


#Search for person within the database and then ask user to join if person is found
# if a person is not found print statement and return to main menu
#search for when signed in
def FindPerson1(cursor,username):
    first_Name = input("Please enter a first name: ")
    last_Name = input("Please enter a last name: ")
    found = False
    
    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        
        if(first_Name == item[2] and last_Name == item[3]):
            print("They are a part of the InCollege system")
            print("Search again: 0")
            user = input()
            if user == "0":
                FindPerson(username)
            else:
                Options(username)
            
    #If they do not find a person they can search again or return to main menu   
    if(found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson(username)
        else:
            Options(username)
        
    print("")
    
#Search when not signed in 
def FindPerson(cursor):
    first_Name = input("Please enter a first name: ")
    last_Name = input("Please enter a last name: ")
    found = False
    
    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:

        if(first_Name == item[2] and last_Name == item[3]):
            print("They are a part of the InCollege system")
            print("Would like to join them and sign up? Press 1")
            user = input()
            if user == "1":
                signUp(cursor,source)
            else:
                Main() 
    #If they do not find a person they can search again or return to main menu   
    if(found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson()
        else:
            Main()
        
    
    print("")


# C++  Java Python SQL JavaScript
def SkillSelect(username):
    print("______________________________________________________________\nC++ | Java | Python | SQL | JavaScript | No Selection\n______________________________________________________________")
    skill = input("Select a skill")
    SelectedSkill(skill.lower(), username)


def SelectedSkill(skill, username):
    if skill == "c++":
        print("under construction")
        Options(username)
    elif skill == "java":
        print("under construction")
        Options(username)
    elif skill == "python":
        print("under construction")
        Options(username)
    elif skill == "sql":
        print("under construction")
        Options(username)
    elif skill == "javascript":
        print("under construction")
        Options(username)
    elif skill == "no selection":
        Options(username)
    else:
        print("Invalid Selection")
        Options(username)


# ====================================================================================================


#connects to the database file that was created
sqlfile = "database.sqlite"
source = sql.connect(sqlfile)
cursor = source.cursor()

#main Function
def Main():

        successStory()
        print("Would you like to sign in or sign up? 0 for sign in, and 1 for sign up: ")
        print("3 for information video | Search Person 4")
        option = input()

        while option != "1" and option != "0" and option != "3" and option != "4":
            input("Incorrect input. 0 for sign in, 1 for sign up, 3 for more information, search 4: ")

        if option == "0":
            status, username = logIn(cursor)
        elif option == "1":
            status, username = signUp(cursor,source)
        elif option == "3":
            status = PlayVideo()
        elif option == "4":
            status = FindPerson()


        if status:
            print("Logged in!")
            # use user to bounce around the functions as needed
            user = Options(username)

        source.close()
if __name__ == "__main__":
    Main()