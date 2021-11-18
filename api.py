import jobs
from os.path import exists, getmtime
from datetime import datetime
import inCollege
import profile
from time import time

# Constants:

API_INPUT_PATH = "apiInputs/" 
API_OUTPUT_PATH = "apiOutputs/"
API_LOG_PATH =  API_OUTPUT_PATH + "api.log"
DELIMITER = " "


# Coordinated running of APIs:

def runAllAPIs(source, cursor):
    allCurrentAPIs = [signUpAPI, newJobsAPI,trainingAPI, jobsAPI, profilesAPI, usersAPI, trainingOutAPI, appliedJobsAPI]
    for api in allCurrentAPIs:
        api(source,cursor)

# Individual APIs:

def signUpAPI(source,cursor):
    input = readFileIfExists("studentAccounts.txt")
    with open(API_LOG_PATH,"a") as logFile:
        if not input: return
        inputKeys = ("username","firstName","lastName","password","membershipCode")
        for accountInfo in input.split("\n=====\n"):
            firstLine, secondLine = accountInfo.split('\n')
            # Assuming when users are signed up with the api their membership is standard
            # I assume this because it's not specified in the document
            inputMappings = dict(zip(inputKeys,firstLine.split(DELIMITER) + [secondLine,"0"]))
            logTimeStamp(f"Starting API signUp with inputs:\n{inputMappings}",logFile)
            try:
                inCollege.signUp(cursor,source,inputMappings)
                print("Signed up successfull\n\n",file=logFile)
            except Exception as e:
                print(f"There was an error signing up user {inputMappings['username']} using the api with exception:\n {e} \n\n",file=logFile)

def newJobsAPI(source,cursor):
    apiName = "newJobs.txt"
    input = readFileIfExists(apiName)
    with open(API_LOG_PATH,"a") as logFile:
        if not input: return
        elif not apiInputsWereUpdated(apiName,source,cursor): return 
        inputKeys = ("title","description","poster","employer","location","salary")
        for jobInfo in input.split("\n=====\n"):
            firstChunck, secondChuck = jobInfo.split('\n&&&\n')
            title = firstChunck.split('\n')[0]
            description = "\n".join(firstChunck.split('\n')[1:])
            inputMappings = dict(zip(inputKeys,[title,description] + secondChuck.split('\n')))
            logTimeStamp(f"Starting API newJobs with inputs:\n{inputMappings}",logFile)
            try:
                jobs.PostJob(cursor,source,None,None,None,inputMappings)
                print("Job posted successfully\n\n",file=logFile)
                updateAPIHistory(apiName,source,cursor)
            except Exception as e:
                print(f"There was an error posting job {inputMappings['title']} using the api with exception:\n {e} \n\n",file=logFile)

def trainingAPI(source,cursor):
    input = readFileIfExists("newtraining.txt")
    with open(API_LOG_PATH,"a") as logFile:
        if not input: return
        for title in input.split("\n"):
            logTimeStamp(f"Starting API training with inputs:\n title:{title}",logFile)
            try:
                with source: cursor.execute(f"INSERT INTO trainings(title) VALUES('{title}')")
                print("Training added successfully\n\n",file=logFile)
            except Exception as e:
                print(f"error while inserting training {title}:\n{e}\n\n",file=logFile) 

def jobsAPI(_,cursor):
    with open(API_OUTPUT_PATH + "MyCollege_jobs.txt","w") as outputFile:
        with open(API_LOG_PATH,"a") as logFile:
            try:
                logTimeStamp(f"Starting API jobs:",logFile)
                cursor.execute("SELECT title,description,employer,location,salary FROM jobs")
                rawQueryResults = cursor.fetchall()
                for result in rawQueryResults:
                    printJob(result,outputFile)
                print("successfully wrote jobs to file\n\n",file=logFile)
            except Exception as e:
                print(f"error while writing jobs to file:\n{e}\n\n",file=logFile)

def profilesAPI(_,cursor):
    with open(API_OUTPUT_PATH + "MyCollege_profiles.txt","w") as outputFile:
        with open(API_LOG_PATH,"a") as logFile:
            try:
                cursor.execute("SELECT belongsTo FROM profiles")
                usersWithProfile = cursor.fetchall()
                for user in usersWithProfile:
                    logTimeStamp(f"Starting API profiles for user {user}",logFile)
                    profile.printProfile(profile.readProfile(cursor,user[0]),outputFile)
                    print("\n=====\n",file=outputFile)
                print("Successfully wrote profiles to file\n\n",file=logFile)
            except Exception as e:
                print(f"error while writing jobs to file:\n{e}\n\n",file=logFile)

def usersAPI(_,cursor):
    with open(API_OUTPUT_PATH + "MyCollege_users.txt","w") as outputFile:
        with open(API_LOG_PATH,"a") as logFile:
            try:
                logTimeStamp(f"Starting API users", logFile)
                cursor.execute("SELECT username, membershipType FROM users")
                users = cursor.fetchall()
                for user in users:
                    print(user[0]," ",user[1], file=outputFile)
                print("Successfully wrote users to file\n\n", file=logFile)
            except Exception as e:
                print(f"error while writing users to file: \n{e}\n\n", file=logFile)

def trainingOutAPI(_, cursor):
    with open(API_OUTPUT_PATH + "MyCollege_training.txt","w") as outputFile:
        with open(API_LOG_PATH,"a") as logFile:
            try:
                cursor.execute("SELECT username, course FROM coursesTaken GROUP BY username, course")
                courses = cursor.fetchall()
                userTemp = ""
                for username in courses:
                    if userTemp != username[0]:
                        if userTemp != "":
                            print("=====", file=outputFile)
                        userTemp = username[0]
                        print(username[0], ":", file=outputFile)
                    print(username[1], file=outputFile)
                print("Successfully wrote training to file\n\n", file=logFile)
            except Exception as e:
                print(f"error while writing training to file: \n{e}\n\n", file=logFile)

def appliedJobsAPI(_, cursor):
    with open(API_OUTPUT_PATH + "MyCollege_appliedJobs.txt","w") as outputFile:
        with open(API_LOG_PATH,"a") as logFile:
            try:
                cursor.execute("SELECT jobs.title, userJobRelation.username, userJobRelation.reasoning FROM jobs, userJobRelation WHERE userJobRelation.jobID = jobs.jobID GROUP BY jobs.jobID, jobs.title, userJobRelation.username, userJobRelation.reasoning")
                jobs = cursor.fetchall()
                jobTemp = ""
                for job in jobs:
                    if job[0] != jobTemp:
                        if jobTemp != "":
                            print("=====", file=outputFile)
                        jobTemp = job[0]
                        print(job[0], ":", file=outputFile)
                    print(job[1], " - reasoning:  ", job[2], file=outputFile)
                print("Successfully wrote userJobs to file\n\n", file=logFile)
            except Exception as e:
                print(f"error while writing training to file: \n{e}\n\n", file=logFile)


# Utility functions:

def readFileIfExists(filename):
    if not exists(API_INPUT_PATH + filename): return None
    with open(API_INPUT_PATH +  filename,"r") as file:
        return file.read()

def logTimeStamp(message, logFile): print(datetime.now().ctime(),"::",message,file=logFile)

def printJob(rawQueryOutput,outputFile):
    jobKeys = ("title","description","employer","location","salary")
    formatedJob = dict(zip(jobKeys,rawQueryOutput))
    for key in formatedJob:
        if formatedJob[key]:
            print(key,":",formatedJob[key],file=outputFile)
    print("\n=====\n",file=outputFile)

def apiInputsWereUpdated(apiName,source,cursor):
    cursor.execute(f"SELECT lastMod FROM apiHistory WHERE apiName = '{apiName}'")
    lastMod = cursor.fetchone()[0]
    return lastMod < getmtime(API_INPUT_PATH + apiName)


def updateAPIHistory(apiName,source,cursor):
    with source: cursor.execute(f"UPDATE apiHistory SET lastMod = {time()} WHERE apiName = '{apiName}'")
