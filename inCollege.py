# Antonio Gonzalez, U57195076
# Kevin Girjanand, U68848880
# Jesse Gonzales, U96407722
# Gabriel Gusmao de Almeida

import time as t
import sqlite3 as sql

import main
import random
from profile import ProfileJob, readProfile
import profile
from connection import Connection, getConnections
import jobs
import message

friendNotificationCount = 0
# Mini function that will capitalize all words in a string
capitalizeWords = lambda words: " ".join([word.capitalize() for word in words.split()])


def logIn(cursor):
    cont = True
    while cont:
        # asks for username and password and attempts to find it in the database
        username = input("What is your username?: ")
        password = input("What is your password?: ")
        cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))

        # if the query is successful, then it logs in, otherwise, it prints an error statement
        data = cursor.fetchall()
        if len(data) == 0:
            print("user does not exist with this username and password combination")
        else:
            loggedIn = True
            cont = False
    return loggedIn, username


def signUp(cursor, source):
    # first checks if the number of rows in Users is 5, if so, that's the maximum number of users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 10:
        print("Unable to sign up. There is already the maximum number of users.")
        loggedIn = False
        username = " "
    else:
        cont = True
        # asks for the username and then searches the database for that username, printing an error if found
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

        # simple input checking for the password
        while cont:
            capital = any(word.isupper() for word in password)
            digit = any(word.isdigit() for word in password)
            if len(password) < 8 or len(
                    password) > 12 or capital == False or digit == False or password.isalnum() == True:
                print(
                    "Invalid option. Password must between 8 and 12 characters, have a digit, capital letter, and a special character")
                password = input("Try another password: ")
            else:
                cont = False

        cont = True

        # Enter first name
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
                            if (firstName == name[2] and lastName == name[3]):
                                print("User already exists")
                                firstName = input("Please enter another first name: ")
                                lastName = input("Please enter another last name: ")
                            else:
                                continue
                        cont = False
        # Select InCollege membership type (standard or plus)
        membershipType = ""
        monthlyBill = 0
        acctSel = input("Would you a standard membership (enter 0) or plus membership (enter 1)?: ")
        if (acctSel == '0'):
            membershipType = "standard"
            monthlyBill = 0
            print("You are now a standard member!\n")
        elif (acctSel == '1'):
            membershipType = "plus"
            monthlyBill += 10
            print("You are now a plus member!\n")
        else:
            membershipType = input("Please enter 0 for standard or 1 for plus:")

        cont = True

        userNotification = firstName + " " + lastName + " has just joined in College"

        addNotification = """
        INSERT into notifications (username, notification) VALUES (?, ?);"""
        cursor.execute(addNotification, (username, userNotification))

        # adds inputs into the Users table, thus making a new row
        # adds inputs into the Users table, thus making a new row
        addVal = """
        INSERT INTO users (username, password, firstName, lastName, membershipType, monthlyBill) VALUES (?, ?, ?, ?, ?, ?);"""

        cursor.execute(addVal, (username, password, firstName, lastName, membershipType, monthlyBill))

        # cursor.execute(addVal,(username, password, firstName, lastName))
        # give user an empty inbox
        cursor.execute(
            "INSERT INTO messages (mess_no, message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?, ?);",
            (-1, "NA", username, "NA", "NA", "TRUE", "NA"))
        # print(username)
        source.commit()
        loggedIn = True
    return loggedIn, username


def PlayVideo(cursor, source):
    print("Video is now playing\n")
    # Waits 4 seconds so user can watch the video then present option to join or go to main menu
    t.sleep(4)
    user = input("Sign up: 0\n")
    if user != "0":
        main.Main()
    else:
        signUp(cursor, source)


def successStory():
    print("Thanks to inCollege I was able to meet with fellow college students and establish connections")
    print("that allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege")
    print(
        "I was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft")
    print("--Alyssa (Arizona)")


def UsefulLink(cursor):
    print("General (1), BrowseInCollege (2), Business Solutions (3), Directories (4)")
    link = input("Please enter a number to go to a link: ")

    if (link == "1"):
        General(cursor)
    elif (link == "2"):
        print("Under construction")
        # main.Main()
    elif (link == "3"):
        print("Under construction")
        # main.Main()
    elif (link == "4"):
        print("Under construction")
        # main.Main()
    else:
        print("Invalid selection")
        UsefulLink(cursor)

    print("")


def General(cursor, source):
    print("Sign Up (1), Help Center (2), About(3), Press (4), Blog(5), Careers(6), and Developers (7)")
    link = input("Please enter a number to go to a link: ")

    if (link == "1"):
        signUp(cursor, source)
    elif (link == "2"):
        print("We're here to help")
        General(cursor)
    elif (link == "3"):
        print(
            "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
        General(cursor)
    elif (link == "4"):
        print("In College Pressroom: Stay on top of the latest news, updates, and reports")
        General(cursor)
    elif (link == "5"):
        print("Under construction")
        General(cursor)
    elif (link == "6"):
        print("Under construction")
        General(cursor)
    elif (link == "7"):
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

    if (link == "1"):
        print("Copyright 2021 InCollege USA. All rights reserved.")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "2"):
        print("An Encouraging online platform for College Students")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "3"):
        print(
            "As part of our commitment to accessibility we continuously audit our products—internally using assistive technology like screen reading software.")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "4"):
        print(
            "Please read this Mobile Application End User License Agreement (“EULA”) carefully before downloading or using the InCollege Inc.")
        print(
            "(“InCollege”) application (“Mobile App”), which allows You to access InCollege’s internet-delivered service (“Subscription Service”)")
        print(
            " from Your mobile device. This EULA forms a binding legal agreement between you (and any other entity on whose behalf you accept these terms)")
        print(
            " (collectively “You” or “Your”) and InCollege (each separately a “Party” and collectively the “Parties”) as of the date you download the Mobile App. ")
        print(
            "Your use of the Mobile App is subject to this EULA and Your use of the Subscription Service will remain subject to the existing agreement governing such use (the “Subscription Agreement”). ")
        print(
            "With respect to the use of the Mobile App, and to the extent the Subscription Agreement conflicts with this EULA, the terms of this EULA will govern and control solely with respect to use of the Mobile App. ")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "5"):
        print("InCollege (“we” or “us” or “our”) respects the privacy of our users (“user” or “you”). ")
        print(
            "This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our mobile application (the “Application”).")
        print(
            "Please read this Privacy Policy carefully. IF YOU DO NOT AGREE WITH THE TERMS OF THIS PRIVACY POLICY, PLEASE DO NOT ACCESS THE APPLICATION.")
        print(
            "We reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the “Last updated” date of this Privacy Policy.")
        print(
            "You are encouraged to periodically review this Privacy Policy to stay informed of updates. You will be deemed to have been made aware of, will be subject to, and will be deemed to have accepted the changes in any revised Privacy Policy")
        print(" by your continued use of the Application after the date such revised Privacy Policy is posted.")
        print("")
        GuestControls(cursor, source, username)
    elif (link == "6"):
        print(
            "Performance cookies: these types of cookies recognise and count the number of visitors to a website and users of an App and to see how users move around ")
        print("in each. This information is used to improve the way the website and App work.")
        print(
            "Functionality cookies: these cookies recognise when you return to a website or App, enable personalised content and recognise and remember your preferences.")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "7"):
        print(
            "You can't post someone else’s private or confidential information without permission or do anything that")
        print(
            "violates someone else's rights, including intellectual property rights (e.g., copyright infringement, trademark infringement, counterfeit, or pirated goods).")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "8"):
        print(
            "This policy governs the use of all InCollege trademarks for any purpose and applies to the entire InCollege system. Consistency")
        print(
            "in the use of Incollege trademarks strengthens their value and our ability to protect them from unauthorized use. ")
        print("")
        InCollegeLink(cursor, source, username)
    elif (link == "9"):
        LanguageSetup(cursor, source, username)
    else:
        print("Invalid selection")
        print("")
        InCollegeLink(cursor, source, username)

    print("")


def GuestControls(cursor, source, username):
    feature = input(
        "Which feature would you like to adjust (type 1 for InCollege Email, 2 for SMS, 3 for Targeted Advertising): ")
    setting = input("Would you like to turn it off or on?: ")

    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if (item[0] == username):
            if (feature == "1"):
                addOption = """
                INSERT INTO users (email) VALUES (?);"""
                cursor.execute(addOption, (setting,))
                source.commit()
            elif (feature == "2"):
                addOption = """
                INSERT INTO users (sms) VALUES (?);"""
                cursor.execute(addOption, (setting,))
                source.commit()
            elif (feature == "3"):
                addOption = """
                INSERT INTO users (ad) VALUES (?);"""
                cursor.execute(addOption, (setting,))
                source.commit()
            else:
                print("Invalid entry")
                GuestControls(cursor, source, username)

    if (feature == "1"):
        if (setting == "off"):
            print("InCollege email turned off")
        elif (setting == "on"):
            print("Incollege email turned on")
    elif (feature == "2"):
        if (setting == "off"):
            print("SMS turned off")
        elif (setting == "on"):
            print("SMS turned on")
    elif (feature == "3"):
        if (setting == "off"):
            print("Targeted advertising turned off")
        elif (setting == "on"):
            print("Targeted advertising turned on")


def LanguageSetup(cursor, source, username):
    language = input("For language of choice, type English or type Spanish: ")
    addOption = """
    INSERT INTO users (language) VALUES (?);"""

    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if (item[0] == username):
            if (language == "English"):
                addOption = """
                INSERT INTO users (language) VALUES (?);"""
                cursor.execute(addOption, (language,))
                source.commit()
            elif (language == "Spanish"):
                addOption = """
                INSERT INTO users (language) VALUES (?);"""
                cursor.execute(addOption, (language,))
                source.commit()
            else:
                print("Invalid entry")
                LanguageSetup(cursor, source, username)

    if language == "English":
        print("English")
    elif language == "Spanish":
        print("Spanish")

# Function will display any notifications the user may have
def Notifications(cursor, source, username):
    cursor.execute("SELECT * FROM notifications")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if(not item[0] == username):
            print(item[1])
            oldNotification = item[1]
            cursor.execute(f"DELETE FROM notifications WHERE notification = '{oldNotification}' ")
            source.commit()

# Function will display any notifications the user may have
def Notifications(cursor, source, username):
    cursor.execute("SELECT * FROM notifications")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if (not item[0] == username):
            print(item[1])
            '''
            oldNotification = item[1]
            cursor.execute(f"DELETE FROM notifications WHERE notification = '{oldNotification}' ")
            source.commit()
            '''

# Functions After Logged In
# ====================================================================================================
# Make an option to go into the profile function.
def Options(cursor, source, username):
    global friendNotificationCount
    if friendNotificationCount == 0:
        cursor.execute("SELECT * FROM friends WHERE friendTwo == ? AND status == 'pending';", (username,))
        items = cursor.fetchall()
        items = list(items)
        if len(items) > 0:
            print("You have some pending friend requests! Go check them at out at View Friend Request!")
        friendNotificationCount = 1

    unread = message.CheckUnread(cursor, source, username)
    if unread == True:
        print("You have unread messages")

    # Check if user has any notifications
    Notifications(cursor, source, username)

    print("Select Option")
    print(
        "=======================================================================================================================================================================")
    UserOpt = input(
        "Search for a Job | Find Someone | Learn Skill | Useful Links | InCollege Links | Profile | Show My Network | View Friend Requests | Send a Friend Request | Messages\n=======================================================================================================================================================================\n")
    # check to see if any jobs have been deleted
    cursor.execute(f"SELECT * FROM userJobRelation WHERE username = '{username}' ")
    saved = cursor.fetchall()
    saved = list(saved)
    for saved in saved:
        # print(saved)
        jobs.CheckJob(cursor, source, username, saved[1])

    UserSelection(UserOpt.lower(), username, cursor, source)


def UserSelection(option, username, cursor, source):
    if option == "search for a job":
        SearchJob(cursor, source, username)
    elif option == "find someone":
        FindPerson1(cursor, username)
    elif option == "learn skill":
        SkillSelect(username, cursor, source)
    elif option == "useful links":
        UsefulLink(cursor)
    elif option == "incollege links":
        InCollegeLink(cursor, source, username)
    elif option == "profile":
        inProfile(cursor, source, username, "")
    elif option == "send a friend request":
        MakeFriend(cursor, source, username)
    elif option == "view friend requests":
        ViewFriendRequest(cursor, source, username)
    elif option == "show my network":
        ShowConnections(cursor, source, username)
    elif option == "messages":
        message.Messages(cursor, source, username)
    else:
        "Invalid Selection"
        Options(cursor, source, username)


def SearchJob(cursor, source, username):
    cursor.execute("SELECT * FROM userJobRelation")
    numJobs = 0
    Jobs = cursor.fetchall()
    Jobs = list(Jobs)
    for Job in Jobs:
        if (Job[2] == 'applied'):
            numJobs = numJobs + 1

    print("You have currently applied for " + str(numJobs) + " jobs")
    post_job = input("Would you like to post a job or delete a job? 'yes', 'remove': ")

    if (post_job == "yes"):
        print("Posting job now")

        cursor.execute("SELECT * FROM users")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if (item[0] == username):
                userFirst = item[2]
                userLast = item[3]

        cursor.execute("SELECT COUNT(*) FROM jobs")
        if (cursor.fetchone()[0] == 10):
            print("Unable to add job. There is already the maximum number of jobs posted.")
        else:
            poster = username
            title = input("Enter a job title: ")
            description = input("Enter a job description: ")
            employer = input("Enter name of employer: ")
            location = input("Enter a location: ")
            salary = input("Enter a salary: ")

            userNotification = "A new job " + str(title) + " has been posted"
            addNotification = """
            INSERT into notifications (username, notification) VALUES (?, ?);"""
            cursor.execute(addNotification, (username, userNotification))

            # adds inputs into the jobs table, thus making a new row
            addJob = """
            INSERT INTO jobs (poster, title, description, employer, location, salary, first, last) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(addJob, (poster, title, description, employer, location, salary, userFirst, userLast))
            source.commit()

            print("To post another job, press 1:")
            user = input()
            if user == "1":
                SearchJob(cursor, source, username)
            else:
                Options(cursor, source, username)
                print("")
    elif (post_job == "remove"):
        print("Which job would you like to remove?")
        cursor.execute("SELECT * FROM jobs WHERE jobs.poster == ?;", (username,))
        items = cursor.fetchall()
        items = list(items)
        # if no jobs to delete go back a menu
        if not items:
            print("no jobs to delete\n")
            SearchJob(cursor, source, username)

        for item in items:
            print("title: " + item[2])

            userNotification = "A job that you had applied for has been deleted - " + str(item[2])
            addNotification = """
            INSERT into notifications (username, notification) VALUES (?, ?);"""
            cursor.execute(addNotification, (username, userNotification))

        remove = input()
        cursor.execute(f"SELECT jobID FROM jobs WHERE jobs.poster == '{username}' AND title == '{remove}' ")
        jobID = cursor.fetchall()
        jobID = list(jobID)
        jobs.DeleteJob(cursor, source, username, jobID[0])
        SearchJob(cursor, source, username)
    else:
        decide = input("Would you like to view jobs instead? 0 for yes: ")
        if decide == '0':
            listJobs(cursor, source, username)
        else:
            Options(cursor, source, username)


def listJobs(cursor, source, username):
    choice = input(
        "Would you like to see saved jobs (0), jobs you've applied for (1), jobs you have yet to apply for (2), or all jobs (3), anything else to return to menu: ")
    # Display saved jobs
    if choice == '0':
        # check to see if any jobs have been deleted
        cursor.execute(f"SELECT * FROM userJobRelation WHERE username = '{username}' ")
        saved = cursor.fetchall()
        saved = list(saved)
        for saved in saved:
            # print(saved)
            print()
            jobs.CheckJob(cursor, source, username, saved[1])

        cursor.execute(
            "SELECT * FROM userJobRelation, jobs WHERE userJobRelation.jobID == jobs.jobID AND userJobRelation.username == ?;",
            (username,))
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if item[2] == 'saved':
                option = input(item[
                                   8] + " is saved. Would you like to view more details (0), apply (1), view next listing (2), Unsave (3) anything else to return to previous screen: ")
                if option == '0':
                    print("title: " + item[8])
                    print("description: " + item[9])
                    print("employer: " + item[10])
                    print("location: " + item[11])
                    print("salary: " + str(item[12]))
                    decide = input("Would you like to apply to this job? Apply: 0, Unsave: 1")
                    if decide == '0':
                        applyForJob(cursor, source, username, item[1])
                    elif decide == '1':
                        jobs.SavedJob(cursor, source, username, item[0])
                    else:
                        listJobs(cursor, source, username)
                elif option == '1':
                    applyForJob(cursor, source, username, item[1])
                elif option == '3':
                    jobs.SavedJob(cursor, source, username, item[1])
                elif option == '2':
                    continue
                else:
                    listJobs(cursor, source, username)
    # applied jobs
    elif choice == '1':
        cursor.execute(
            "SELECT * FROM userJobRelation, jobs WHERE userJobRelation.jobID == jobs.jobID AND userJobRelation.username == ?;",
            (username,))
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if item[2] == 'applied':
                print("You've applied to " + item[8] + " with " + item[10] + " at " + item[11])
    # Unapplied job
    elif choice == '2':
        cursor.execute(
            "SELECT * FROM jobs WHERE jobID NOT IN (SELECT userJobRelation.jobID FROM userJobRelation, jobs AS J WHERE userJobRelation.jobID = J.jobID AND userJobRelation.status = 'applied' AND userJobRelation.username == ?);",
            (username,))
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if item[1] == username:
                continue
            option = input(item[
                               2] + ": You have not applied yet for this position.\n Would you like to view more details (0) apply (1), or go to the next listing (2), save for later (3), anything else to return to previous screen: ")
            if option == '0':
                print("title: " + item[2])
                print("description: " + item[3])
                print("employer: " + item[4])
                print("location: " + item[5])
                print("salary: " + str(item[6]))
                decide = input(
                    "Would you like to apply for this job? 0 for yes, 1 for next listing, 3 for save, anything else to return to previous screen: ")
                if decide == '0':
                    applyForJob(cursor, source, username, item[0])
                elif decide == '1':
                    continue
                else:
                    listJobs(cursor, source, username)
            elif option == '1':
                applyForJob(cursor, source, username, item[0])
            elif option == '2':
                continue
            elif option == '3':
                jobs.SavedJob(cursor, source, username, item[0])
            else:
                listJobs(cursor, source, username)
    # elif choice == '3:
    else:
        Options(cursor, source, username)
    listJobs(cursor, source, username)


def applyForJob(cursor, source, username, jobID):
    cont = True
    graduation = input("What is your graduation date? (mm/dd/yyyy): ")
    while cont:
        if graduation[2] != '/' or graduation[5] != '/' or len(graduation) != 10:
            graduation = input("Invalid format. What is your graduation date? (mm/dd/yyyy): ")
            continue
        graduation = graduation.replace("/", "")
        if (not graduation.isnumeric()) or len(graduation) != 8:
            graduation = input("Invalid format. What is your graduation date? (mm/dd/yyyy): ")
            continue
        else:
            break

    start = input("What is your expected start date? (mm/dd/yyyy): ")
    while cont:
        if start[2] != '/' or start[5] != '/' or len(start) != 10:
            start = input("Invalid format. What is your expected start date? (mm/dd/yyyy): ")
            continue
        start = start.replace("/", "")
        if (not start.isnumeric()) or len(start) != 8:
            start = input("Invalid format. What is your expected start date? (mm/dd/yyyy): ")
            continue
        else:
            break
    reason = input("In a paragraph, explain why you think you'd be a good fit for this job: ")

    cursor.execute("SELECT * FROM userJobRelation WHERE userJobRelation.jobID == ? AND userJobRelation.username == ?;",
                   (jobID, username))
    items = cursor.fetchall()
    items = list(items)
    if len(items) != 0:
        for item in items:
            cursor.execute(
                "UPDATE userJobRelation SET graduation_date = ? WHERE userJobRelation.jobID == ? AND userJobRelation.username == ?;",
                (graduation, jobID, username))
            cursor.execute(
                "UPDATE userJobRelation SET start_date = ? WHERE userJobRelation.jobID == ? AND userJobRelation.username == ?;",
                (start, jobID, username))
            cursor.execute(
                "UPDATE userJobRelation SET reasoning = ? WHERE userJobRelation.jobID == ? AND userJobRelation.username == ?;",
                (reason, jobID, username))
            cursor.execute(
                "UPDATE userJobRelation SET status = 'applied' WHERE userJobRelation.jobID == ? AND userJobRelation.username == ?;",
                (jobID, username))
            source.commit()
    else:
        cursor.execute(
            "INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, 'applied', ?, ?, ?);",
            (username, jobID, graduation, start, reason))
        source.commit()
    print("Successfully applied!")
    Options(cursor, source, username)


# Search for person within the database and then ask user to join if person is found
# if a person is not found print statement and return to main menu
# search for when signed in
def FindPerson1(cursor, username, source):
    first_Name = input("Please enter a first name: ")
    last_Name = input("Please enter a last name: ")
    found = False

    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:

        if (first_Name == item[2] and last_Name == item[3]):
            print("They are a part of the InCollege system")
            print("Search again: 0")
            user = input()
            if user == "0":
                FindPerson1(cursor, username, source)
            else:
                Options(cursor, source, username)

    # If they do not find a person they can search again or return to main menu
    if (found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson1(cursor, source, username)
        else:
            Options(cursor, source, username)

    print("")


# View friends. Assumes that we want to display the friend's username
def ShowConnections(cursor, source, username):
    # Check if user has plus membership
    cursor.execute("SELECT * FROM users")
    names = cursor.fetchall()
    names = list(names)
    hadResult = False
    for name in names:
        if (name[0] == username):
            if (name[8] == "plus"):
                print("Would you like to send a message? type 'message' ")
                choice = input()
                choice.lower()
                if choice == "message":
                    message.SendMessage(cursor, source, username, "")
            elif (name[8] == "standard"):
                connections = getConnections(cursor, source, username)
                hadResult = False
                for connection in connections:
                    if connection.status != "pending":
                        hadResult = True
                        print(f"Connection's name: {connection.friend}")
                        connectionProfile = readProfile(cursor, connection.friend)
                        if connectionProfile:
                            print("This connection has a profile, would you like to look at it? 'yes' to view it")
                            choice = input()
                            if choice == 'yes':
                                printProfile(connectionProfile)
                        print("Would you like to disconnect with this person? type 'disconnect' if you would like it.")
                        print("Would you like to send a message? type 'message' ")
                        choice = input()
                        choice.lower()
                        if choice == "disconnect":
                            exFriend = connection.friend
                            connection.disconnect()
                            print(f"You disconnected with {exFriend}")
                        elif choice == "message":
                            message.SendMessage(cursor, source, username, connection.friend)

    if not hadResult:
        print("No connections were found")
    Options(cursor, source, username)


# send a friend request
def MakeFriend(cursor, source, username):
    last_name = input("Please enter a last name, 0 for none: ")
    major = input("Please enter a major, 0 for none: ")
    university = input("Please enter a university, 0 for none: ")

    if last_name == '0' and major == '0' and university == '0':
        choice = input(
            "Invalid. Please enter at least one name, major or university. Would you like to search again? 0 for yes ")
        if choice == '0':
            MakeFriend(cursor, source, username)
        else:
            Options(cursor, source, username)
    found = False
    if major == '0' and university == '0':
        cursor.execute("SELECT * FROM users")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if last_name == item[3]:
                cursor.execute(
                    "SELECT * FROM friends WHERE (friendOne == ? AND friendTwo == ?) OR (friendOne == ? AND friendTwo == ?);",
                    (username, item[0], item[0], username))
                values = cursor.fetchall()
                values = list(values)
                if len(values) == 1:
                    continue
                if username != item[0]:
                    decision = input(item[2] + ' ' + item[
                        3] + ' is in the College System? Would you like to add this person? 0 for yes: ')
                    if decision == '0':
                        cursor.execute("INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, 'pending');",
                                       (username, item[0]))
                        source.commit()
                        print("Friend Request Sent")
    else:
        cursor.execute("SELECT * FROM users, profiles WHERE profiles.belongsTo == users.username;")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if (last_name == '0' or last_name == item[3]) and (major == '0' or major == item[10]) and (
                    university == '0' or university == item[11]):
                cursor.execute(
                    "SELECT * FROM friends WHERE (friendOne == ? AND friendTwo == ?) OR (friendOne == ? AND friendTwo == ?);",
                    (username, item[0], item[0], username))
                values = cursor.fetchall()
                values = list(values)
                if len(values) == 1:
                    continue
                if username != item[0]:
                    decision = input(item[2] + ' ' + item[
                        3] + ' is in the College System. Would you like to add this person? 0 for yes: ')
                    if decision == '0':
                        cursor.execute("INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, 'pending');",
                                       (username, item[0]))
                        source.commit()
                        print("Friend Request Sent")
    Options(cursor, source, username)


# view any incoming friend requests or pending friend requests
def ViewFriendRequest(cursor, source, username):
    choice = input("View Incoming Friend Requests or Pending Requests Sent? 0 for incoming: ")
    if choice == '0':
        cursor.execute("SELECT * FROM friends WHERE friendTwo == ? AND status == 'pending';", (username,))
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            option = input("Would you like to accept " + item[0] + "? 0 for accept: ")
            if option == '0':
                cursor.execute("UPDATE friends SET status='active' WHERE friendOne == ? AND friendTwo == ?;",
                               (item[0], username))
                source.commit()
            else:
                cursor.execute("DELETE FROM friends WHERE friendOne == ? AND friendTwo == ?;", (item[0], username))
                source.commit()
    else:
        cursor.execute("SELECT * FROM friends WHERE friendOne == ? AND status == 'pending'", (username,))
        items = cursor.fetchall()
        items = list(items)
        print("Pending Requests Sent: ")
        for item in items:
            print(item[1])

    decision = input("Would you like to return to the main menu? 0 for yes: ")
    if decision == '0':
        Options(cursor, source, username)
    else:
        ViewFriendRequest(cursor, source, username)


# search when not signed in
def FindPerson(cursor, source):
    first_Name = input("Please enter a first name: ")
    last_Name = input("Please enter a last name: ")
    found = False

    cursor.execute("SELECT * FROM users")
    items = cursor.fetchall()
    items = list(items)
    for item in items:
        if (first_Name == item[2] and last_Name == item[3]):
            print("They are a part of the InCollege system")
            print("Would like to join them and sign up? Press 1")
            user = input()
            if user == "1":
                signUp(cursor, source)
            else:
                main.Main()
                # If they do not find a person they can search again or return to main menu
    if (found == False):
        print("They are not yet a part of the InCollege system")
        print("Search again: 0")
        user = input()
        if user == "0":
            FindPerson(cursor)
        else:
            main.Main()

    print("")


# Profile creation
def inProfile(cursor, source, username):
    result = profile.readProfile(cursor, username)
    if not result:
        print("You don't have a profile, would you like to create one? Type 'yes' to create it")
        choice = input()
        if choice.lower() == "yes":
            newProfile = profile.Profile(username)
            EditProfile(newProfile, cursor)
            profile.createProfile(cursor, source, newProfile)
        Options(cursor, source, username)
        # inform user they don't have a profile and offer options to create or go back
    else:
        printProfile(result)
        print("Would you like to update your profile? type 'yes' to update it")

        choice = input()
        if choice.lower() == "yes":
            EditProfile(result, cursor)
            profile.updateProfile(cursor, source, result)
        Options(cursor, source, username)


# Will get the desired changes to profile and return the profile object
# added cursor so that test_inCollege can pass input to the questions
def EditProfile(profile, cursor):
    if profile.title:
        message = f"The title of your profile is {profile.title}. Would you like to change it? 'yes' to change it"
    else:
        message = f"You don't have a title for your profile. Would you like to create it? 'yes' to create it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.title = input("Enter the title ")
    if profile.major:
        message = f"The major of your profile is {profile.major}. Would you like to change it? 'yes' to change it"
    else:
        message = f"You don't have a major for your profile. Would you like to create it? 'yes' to create it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.major = input("Enter the major ")
    if profile.university:
        message = f"The university of your profile is {profile.university}. Would you like to change it? 'yes' to change it"
        print(message)
    else:
        message = f"You don't have a university for your profile. Would you like to create it? 'yes' to create it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.university = input("Enter the university ")
    if profile.about:
        message = f"The about of your profile is {profile.about}. Would you like to change it? 'yes' to change it"
    else:
        message = f"You don't have about for your profile. Would you like to create it? 'yes' to create it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.about = input("Enter the about ")
    print("Experience Section:")
    for i, job in enumerate(profile.experience):
        printProfileJob(job, i)
        print("Would you like to edit this job? 'yes' to edit")
        choice = input()
        if choice == "yes":
            editProfileJob(profile.experience[i])
    if len(profile.experience) < 3:
        print("Would you like to add another job? 'yes' to add it")
        choice = input()
        if choice == 'yes':
            newJob = ProfileJob()
            editProfileJob(newJob)
            profile.experience.append(newJob)
    print("Education Section: ")
    if profile.degree:
        message = f"The degree of your profile is {profile.degree}. Would you like to change it? 'yes' to change it"
    else:
        message = f"You don't information about your degree. Would you like to add it? 'yes' to add it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.about = input("Enter the degree ")
    if profile.yearsAtUni:
        message = f"The years attended of your profile is {profile.yearsAtUni}. Would you like to change it? 'yes' to change it"
    else:
        message = f"You don't have specified how many years you attended your university. Would you like to create it? Type 'yes' to create it"
    print(message)
    choice = input()
    if choice == "yes":
        profile.about = input("Enter the years attended ")


def editProfileJob(job):
    attrs = job.__dict__
    for key in attrs:
        if attrs[key]:
            message = f"The {key} of this job is {attrs[key]}. Would you like to change it? 'yes' to change it"
        else:
            message = f"This job doesn't have a {key}. Would you like to create it? Type 'yes' to create it"
        print(message)
        choice = input()
        if choice == "yes":
            profile.about = input(f"Enter the {key}")
        elif choice == "no":
            pass
        else:
            print("invalid input")


def printProfileJob(job, index):
    print(f"Job {index + 1}:")
    print("-------")
    attrs = job.__dict__
    for key in attrs:
        print(f"{key}: {attrs[key]}")


def printProfile(profile):
    print("\nProfile: ")
    print("-------------")
    print(f"Title: {profile.title}")
    print(f"Major: {profile.major}")
    print(f"University: {profile.university}")
    print(f"About: {profile.about}")
    print(f"\nExperience Section:")
    print("-------------------------")
    for i, job in enumerate(profile.experience):
        printProfileJob(job, i)
    print("\nEducation Section:")
    print("-------------------------")
    print(f"School Name: {profile.university}")
    print(f"Degree: {profile.degree}")
    print(f"Years attedend: {profile.yearsAtUni}")

    # Handle the experience case
def profileMessage(cursor,username):
    cursor.execute(f"SELECT count(belongsTo) FROM profiles WHERE belongsTo='{username}' ")  
    result = cursor.fetchone()
    if result[0] == 0: {
        print("Dont forget to create a profile")
    }

def waitingMessages(cursor,username):
    cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}' ")  
    result = cursor.fetchone()
    if result[0] >= 1 and result[0] != username: {
        print("You have messages waiting for you")
    }

# C++  Java Python SQL JavaScript
def SkillSelect(username, cursor, source):
    print(
        "______________________________________________________________\nC++ | Java | Python | SQL | JavaScript | No Selection\n______________________________________________________________")
    skill = input("Select a skill")
    SelectedSkill(skill.lower(), username, cursor, source)


def SelectedSkill(skill, username, cursor, source):
    if skill == "c++":
        print("under construction")
        Options(cursor, source, username)
    elif skill == "java":
        print("under construction")
        Options(cursor, source, username)
    elif skill == "python":
        print("under construction")
        Options(cursor, source, username)
    elif skill == "sql":
        print("under construction")
        Options(cursor, source, username)
    elif skill == "javascript":
        print("under construction")
        Options(cursor, source, username)
    elif skill == "no selection":
        Options(cursor, source, username)
    else:
        print("Invalid Selection")
        Options(cursor, source, username)