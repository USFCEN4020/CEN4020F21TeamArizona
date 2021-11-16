import jobs
from os.path import exists
from datetime import datetime
import inCollege
import profile

# Constants:

API_INPUT_PATH = "apiInputs/" 
API_OUTPUT_PATH = "apiOutputs/"
API_LOG_PATH =  API_OUTPUT_PATH + "api.log"
DELIMITER = " "


# Coordinated running of APIs:

def runAllAPIs(source, cursor):
    allCurrentAPIs = [signUpAPI, newJobsAPI,trainingAPI, jobsAPI, profilesAPI]
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
    input = readFileIfExists("newJobs.txt")
    with open(API_LOG_PATH,"a") as logFile:
        if not input: return
        inputKeys = ("title","description","poster name","employer","location","salary")
        for jobInfo in input.split("\n=====\n"):
            firstChunck, secondChuck = jobInfo.split('\n&&&\n')
            title = firstChunck.split('\n')[0]
            description = "\n".join(firstChunck.split('\n')[1:])
            inputMappings = dict(zip(inputKeys,[title,description] + secondChuck.split('\n')))
            logTimeStamp(f"Starting API newJobs with inputs:\n{inputMappings}",logFile)
            try:
                jobs.PostJob(cursor,source,None,None,None,inputMappings)
                print("Job posted successfully\n\n",file=logFile)
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