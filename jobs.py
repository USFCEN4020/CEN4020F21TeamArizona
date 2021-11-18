#InCollege job management should be able to 
# delete a job, notify students job has been removed, 
# and next time they visit job section they get notified job has been deleted
import inCollege
from api import jobsAPI
from sys import stdout
from api import appliedJobsAPI

def CheckJob(cursor, source, username, jobID):
    cursor.execute(f"SELECT * FROM jobs WHERE jobID = '{jobID}'")
    job = cursor.fetchall()
    #print(jobID)
    if not job:
        print(f"Saved job '{jobID}' was deleted")
        cursor.execute(f"DELETE FROM userJobRelation WHERE username = '{username}' AND jobID ='{jobID}' ")
        source.commit()
        jobsAPI(source,cursor)


def DeleteJob(cursor, source, username, jobID):
    #print("Delete jobs here")
    ID = jobID[0]
    print(f"Delete Job: '{ID}' ")
    cursor.execute(f"DELETE FROM jobs WHERE jobID = '{ID}' ")
    cursor.execute(f"DELETE FROM profileJobs WHERE jobID = '{ID}'")
    source.commit()
    jobsAPI(source,cursor)
    SearchJob(cursor, source, username)
    
    
#InCollege job management should be able to save job
# User: mark job as saved, genereate list of saved jobs 
# should be able to unmark saved jobs. THe list of saved jobs will be retained
# can be displayed next time they log in  
def SavedJob(cursor, source, username, jobID): 
    #print("Saved jobs here") 
    #print(jobID)
    #Query the database with user and job id for userJobRelation
    # (FK Username, FK Jobid, status, grad_date, start, reasoning) PK Username, JobID
    print("Would you like to save a job (1), Unsave the job (2)")
    choice = input()
    if choice == '1':
        cursor.execute("INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, ?, ?, ?, ?);",
            (username, jobID, "saved", "NA", "NA", "NA"))
        source.commit()
        jobsAPI(source,cursor)
    elif choice == '2':
        cursor.execute(f"DELETE FROM userJobRelation WHERE username = '{username}' AND jobID ='{jobID}' ")


def PostJob(cursor,source,username,userFirst,userLast,apiInputs=None):
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if (cursor.fetchone()[0] == 10):
        if apiInputs: raise Exception("Exception: There are already a maximum number of jobs")
        print("Unable to add job. There is already the maximum number of jobs posted.")
    elif not apiInputs:
        poster = username
        title = input("Enter a job title: ")
        description = input("Enter a job description: ")
        employer = input("Enter name of employer: ")
        location = input("Enter a location: ")
        salary = input("Enter a salary: ")
    else:
        poster = username
        title = apiInputs["title"]
        description = apiInputs["description"]
        employer = apiInputs["employer"]
        location = apiInputs["location"]
        salary = apiInputs["salary"]

        userNotification = "A new job " + str(title) + " has been posted"
        addNotification = """
        INSERT into notifications (username, notification) VALUES (?, ?);"""
        cursor.execute(addNotification, (username, userNotification))

        # adds inputs into the jobs table, thus making a new row
        addJob = """
        INSERT INTO jobs (poster, title, description, employer, location, salary, first, last) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(addJob, (poster, title, description, employer, location, salary, userFirst, userLast))
        source.commit()
        jobsAPI(source,cursor)

        if not apiInputs:
            print("To post another job, press 1:")
            user = input()
            if user == "1":
                SearchJob(cursor, source, username)
            else:
                inCollege.Options(cursor, source, username)
                print("")
        
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
        PostJob(cursor,source,username,userFirst,userLast)
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
        DeleteJob(cursor, source, username, jobID[0])
        SearchJob(cursor, source, username)
    else:
        decide = input("Would you like to view jobs instead? 0 for yes: ")
        if decide == '0':
            listJobs(cursor, source, username)
        else:
            inCollege.Options(cursor, source, username)


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
            CheckJob(cursor, source, username, saved[1])

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
                        SavedJob(cursor, source, username, item[0])
                    else:
                        listJobs(cursor, source, username)
                elif option == '1':
                    applyForJob(cursor, source, username, item[1])
                elif option == '3':
                    SavedJob(cursor, source, username, item[1])
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
                SavedJob(cursor, source, username, item[0])
            else:
                listJobs(cursor, source, username)
    # elif choice == '3:
    else:
        inCollege.Options(cursor, source, username)
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
            jobsAPI(source,cursor)
            appliedJobsAPI(source, cursor)
    else:
        cursor.execute(
            "INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, 'applied', ?, ?, ?);",
            (username, jobID, graduation, start, reason))
        source.commit()
        appliedJobsAPI(source, cursor)
        jobsAPI(source,cursor)
    print("Successfully applied!")
    inCollege.Options(cursor, source, username)