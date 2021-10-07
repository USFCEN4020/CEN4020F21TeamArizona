#Antonio Gonzalez, U57195076
#Kevin Girjanand, U68848880
#Jesse Gonzales, U96407722

import time as t
import sqlite3 as sql
import main

#connects to the database file that was created
sqlfile = "database.sqlite"
source = sql.connect(sqlfile)
cursor = source.cursor()

#Mini function that will capitalize all words in a string
capitalizeWords = lambda words : " ".join([word.capitalize() for word in words.split()])

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
        main.Main()
    else:
        signUp(cursor, source)
        
def successStory():
    print("Thanks to inCollege I was able to meet with fellow college students and establish connections")
    print("that allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege")
    print("I was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft")
    print("--Alyssa (Arizona)")
    
def UsefulLink(cursor):
    print("General (1), BrowseInCollege (2), Business Solutions (3), Directories (4)")
    link = input("Please enter a number to go to a link: ")
    
    if(link == "1"):
        General(cursor)
    elif(link == "2"):
        print("Under construction")
        #main.Main()
    elif(link == "3"):
        print("Under construction")
        #main.Main()
    elif(link == "4"):
        print("Under construction")
        #main.Main()
    else:
        print("Invalid selection")
        UsefulLink(cursor)
    
    print("")
    
    
def General(cursor):
    print("Sign Up (1), Help Center (2), About(3), Press (4), Blog(5), Careers(6), and Developers (7)")
    link = input("Please enter a number to go to a link: ")
    
    if(link == "1"):
        signUp(cursor, source)
    elif(link == "2"):
        print("We're here to help")
        General(cursor)
    elif(link == "3"):
        print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
        General(cursor)
    elif(link == "4"):
        print("In College Pressroom: Stay on top of the latest news, updates, and reports")
        General(cursor)
    elif(link == "5"):
        print("Under construction")
        General(cursor)
    elif(link == "6"):
        print("Under construction")
        General(cursor)
    elif(link == "7"):
        print("Under construction")
        General(cursor)
    else:
        print("Invalid selection")
        UsefulLink(cursor)    
    
    
def InCollegeLink(cursor, source, username):
    print("Copyright Notice (1), About (2), Accessibility (3)")
    print("User Agreement (4), Privacy Policy (5), Cookie Policy (6)")
    print("Copyright Policy (7), Brand Policy (8), Languages (9)")
    link = input("Please enter a number to go to a link: ")
    
    if(link == "1"):
        print("Copyright 2021 InCollege USA. All rights reserved.")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "2"):
        print("An Encouraging online platform for College Students")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "3"):
        print("As part of our commitment to accessibility we continuously audit our products—internally using assistive technology like screen reading software.")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "4"):
        print("Please read this Mobile Application End User License Agreement (“EULA”) carefully before downloading or using the InCollege Inc.")
        print("(“InCollege”) application (“Mobile App”), which allows You to access InCollege’s internet-delivered service (“Subscription Service”)")
        print(" from Your mobile device. This EULA forms a binding legal agreement between you (and any other entity on whose behalf you accept these terms)")
        print(" (collectively “You” or “Your”) and InCollege (each separately a “Party” and collectively the “Parties”) as of the date you download the Mobile App. ")
        print("Your use of the Mobile App is subject to this EULA and Your use of the Subscription Service will remain subject to the existing agreement governing such use (the “Subscription Agreement”). ")
        print("With respect to the use of the Mobile App, and to the extent the Subscription Agreement conflicts with this EULA, the terms of this EULA will govern and control solely with respect to use of the Mobile App. ")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "5"):
        print("InCollege (“we” or “us” or “our”) respects the privacy of our users (“user” or “you”). ")
        print("This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our mobile application (the “Application”).")
        print("Please read this Privacy Policy carefully. IF YOU DO NOT AGREE WITH THE TERMS OF THIS PRIVACY POLICY, PLEASE DO NOT ACCESS THE APPLICATION.")
        print("We reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the “Last updated” date of this Privacy Policy.")
        print("You are encouraged to periodically review this Privacy Policy to stay informed of updates. You will be deemed to have been made aware of, will be subject to, and will be deemed to have accepted the changes in any revised Privacy Policy")
        print(" by your continued use of the Application after the date such revised Privacy Policy is posted.")
        print("")
        GuestControls(cursor, source, username)
    elif(link == "6"):
        print("Performance cookies: these types of cookies recognise and count the number of visitors to a website and users of an App and to see how users move around ")
        print("in each. This information is used to improve the way the website and App work.")
        print("Functionality cookies: these cookies recognise when you return to a website or App, enable personalised content and recognise and remember your preferences.")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "7"):
        print("You can't post someone else’s private or confidential information without permission or do anything that")
        print("violates someone else's rights, including intellectual property rights (e.g., copyright infringement, trademark infringement, counterfeit, or pirated goods).")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "8"):
        print("This policy governs the use of all InCollege trademarks for any purpose and applies to the entire InCollege system. Consistency")
        print("in the use of Incollege trademarks strengthens their value and our ability to protect them from unauthorized use. ")
        print("")
        InCollegeLink(cursor, source, username)
    elif(link == "9"):
        LanguageSetup(cursor, source, username)
    else:
        print("Invalid selection")
        print("")
        InCollegeLink(cursor, source, username)  
    
    print("")


def GuestControls(cursor, source, username):
    feature = input("Which feature would you like to adjust (type 1 for InCollege Email, 2 for SMS, 3 for Targeted Advertising): ")
    setting = input("Would you like to turn it off or on?: ")
    
    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if(item[0] == username):
            if(feature == "1"):
                addOption = """
                INSERT INTO users (email) VALUES (?);"""
                cursor.execute(addOption,(setting,))
                source.commit()
            elif(feature == "2"):
                addOption = """
                INSERT INTO users (sms) VALUES (?);"""
                cursor.execute(addOption,(setting,))
                source.commit()
            elif(feature == "3"):
                addOption = """
                INSERT INTO users (ad) VALUES (?);"""
                cursor.execute(addOption,(setting,))
                source.commit()
            else:
                print("Invalid entry")
                GuestControls(cursor, source, username)
    
    
    if(feature == "1"):
        if(setting == "off"):
            print("InCollege email turned off")
        elif(setting == "on"):
            print("Incollege email turned on")
    elif(feature == "2"):
        if(setting == "off"):
            print("SMS turned off")
        elif(setting == "on"):
            print("SMS turned on")
    elif(feature == "3"):
        if(setting == "off"):
            print("Targeted advertising turned off")
        elif(setting == "on"):
            print("Targeted advertising turned on")
    
    
        
def LanguageSetup(cursor, source, username):
    language = input("For language of choice, type English or type Spanish: ")
    addOption = """
    INSERT INTO users (language) VALUES (?);"""

    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if(item[0] == username):
            if(language == "English"):
                addOption = """
                INSERT INTO users (language) VALUES (?);"""
                cursor.execute(addOption,(language,))
                source.commit()
            elif(language == "Spanish"):
                addOption = """
                INSERT INTO users (language) VALUES (?);"""
                cursor.execute(addOption,(language,))
                source.commit()
            else:
                print("Invalid entry")
                LanguageSetup(cursor, source, username)
    
    if language == "English":
        print("English")
    elif language == "Spanish":
        print("Spanish")


# Functions After Logged In
# ====================================================================================================
#Make an option to go into the profile function. 
def Options(cursor, source, username):
    print("Select Option")
    print("============================================================")
    UserOpt = input(
        "Search for a Job | Find Someone | Learn Skill | Useful Links | InCollege Links\n============================================================\n")

    UserSelection(UserOpt.lower(), username)

def UserSelection(option, username):
    if option == "search for a job":
        SearchJob(cursor,source,username)
    elif option == "find someone":
        FindPerson(cursor)
    elif option == "learn skill":
        SkillSelect(username)
    elif option == "useful links":
        UsefulLink(cursor)
    elif option == "incollege links":
        InCollegeLink(cursor, source, username)
    else:
        "Invalid Selection"
        Options(cursor, source, username)

def SearchJob(cursor,source,username):
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
                SearchJob(cursor,source,username)
            else:
                Options(cursor,source,username)
                print("")
    else:       
        Options(cursor,source,username)


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
                FindPerson(cursor)
            else:
                Options(username)
            
    #If they do not find a person they can search again or return to main menu   
    if(found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson(cursor)
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
                main.Main() 
    #If they do not find a person they can search again or return to main menu   
    if(found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson(cursor)
        else:
            main.Main()
        
    
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

def updateProfile(cursor,username,fields={}):
    pass
