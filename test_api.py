import inCollege
import sqlite3 as sql
import pytest
import profile
import connection 
import jobs
import message
import learning
import api
from message import Messages
from os.path import exists, getmtime
from datetime import datetime
from time import time
from os.path import exists

API_INPUT_PATH = "apiInputs/" 
API_TESTINPUT_PATH = "apiTestInputs/"
API_OUTPUT_PATH = "apiOutputs/"
API_TESTOUTPUT_PATH = "apiTestOutputs/"
API_LOG_PATH =  API_OUTPUT_PATH + "api.log"
DELIMITER = " "

# Creating a test database to not interfere with data from the primary one

@pytest.fixture
def testDB():
    source = sql.connect(":memory:")
    cursor = source.cursor()
    createTable = """

    CREATE TABLE users
    (
        username TEXT PRIMARY KEY,
        password TEXT,
        firstName TEXT,
        lastName TEXT,
        email TEXT,
        sms TEXT,
        ad TEXT,
        language TEXT,
        membershipType TEXT,
        monthlyBill INTEGER
    );

    """


    createJobTable = """

    CREATE TABLE jobs
    (
        jobID INTEGER AUTO_INCREMENT,
        poster TEXT,
        title TEXT,
        description TEXT,
        employer TEXT,
        location TEXT,
        salary INTEGER,
        first TEXT,
        last TEXT,
        PRIMARY KEY(jobID)
        CONSTRAINT poster
            FOREIGN KEY (poster) REFERENCES users(username)
    );
    """

    createUserJobRelation = """
        CREATE TABLE userJobRelation
        (
            username TEXT,
            jobID INTEGER,
            status TEXT,
            graduation_date TEXT,
            start_date TEXT,
            reasoning TEXT,
            CONSTRAINT username
                FOREIGN KEY(username) REFERENCES users(username),
            CONSTRAINT jobID
                FOREIGN KEY(jobID) REFERENCES jobs(jobID),
            PRIMARY KEY(username, jobID)
        );
    """

    createProfileJobsTable = """
        
        CREATE TABLE profileJobs
        (
            jobID INTEGER PRIMARY KEY,
            fromUser TEXT,
            title TEXT,
            employer TEXT,
            location TEXT,
            dateStarted DATE,
            dateEnded DATE,
            description TEXT,
            CONSTRAINT fromUser
                FOREIGN KEY(fromUser) REFERENCES users(username)
                ON DELETE CASCADE

        );

    """

    createProfileTable = """

    CREATE TABLE profiles
    (
        belongsTo TEXT,
        title TEXT,
        major TEXT,
        university  TEXT,
        about TEXT,
        degree TEXT,
        yearsAtUni INTEGER,
        CONSTRAINT belongsTo
            FOREIGN KEY(belongsTo) REFERENCES users(username)
            ON DELETE CASCADE,
        PRIMARY KEY(belongsTo)
    );

    """


    createFriendTable = """
    CREATE TABLE friends
    (
        friendOne TEXT,
        friendTwo TEXT,
        status TEXT,
        CONSTRAINT friendOne
            FOREIGN KEY(friendOne) REFERENCES users(username),
        CONSTRAINT friendTwo
            FOREIGN KEY(friendTwo) REFERENCES users(username),
        PRIMARY KEY(friendOne, friendTwo)
    );
    """

    createMessages = """
    CREATE TABLE messages
    (
        mess_no INTEGER AUTO_INCREMENT,
        message TEXT,
        receiver TEXT,
        sender TEXT, 
        status TEXT,
        is_Friend TEXT,
        subject TEXT, 
        CONSTRAINT reciever
            FOREIGN KEY(receiver) REFERENCES users(username),
        CONSTRAINT sender
            FOREIGN KEY(sender) REFERENCES users(username),
        PRIMARY KEY(mess_no, subject, receiver)

    );
    """
    createNotifications = """
    CREATE TABLE notifications
    (
        username TEXT,
        notification TEXT
    );
    """

    createCoursesTaken = """
    CREATE TABLE coursesTaken
    (
        username TEXT,
        course TEXT,
        CONSTRAINT username
            FOREIGN KEY(username) REFERENCES users(username)
        PRIMARY KEY(username,course)
    );
    """
    createTraining = """
        CREATE TABLE trainings
        (
            title TEXT,
            PRIMARY KEY(title)
        )
    """

    createAPIHistory = """
    CREATE TABLE apiHistory
    (
        apiName TEXT,
        lastMod INTEGER,
        PRIMARY KEY(apiName)
    );
    """

    cursor.execute(createTraining)
    initialTrainings = ["Training and Education","Help Desk","Business Analysis and Strategy","Security"]
    for training in initialTrainings:
        cursor.execute(f"INSERT INTO trainings(title) VALUES('{training}')")
    cursor.execute(createAPIHistory)
    cursor.execute("INSERT INTO apiHistory(apiName,lastMod) VALUES('newJobs.txt',0)")
    cursor.execute("INSERT INTO apiHistory(apiName,lastMod) VALUES('newtraining.txt',0)")
    cursor.execute("INSERT INTO apiHistory(apiName,lastMod) VALUES('studentAccounts.txt',0)")
    cursor.execute(createTable)
    cursor.execute(createJobTable)
    cursor.execute(createProfileTable)
    cursor.execute(createProfileJobsTable)
    cursor.execute(createFriendTable)
    cursor.execute(createUserJobRelation)
    cursor.execute(createMessages)
    cursor.execute(createNotifications)
    cursor.execute(createCoursesTaken)
    source.commit()
    return cursor, source


def test_MyCollegeJobs(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO jobs (title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?)',
                    ('Software Engineer', 'Become a Software Engineer today with Pokemon! Its one of the best positions out there! Trust us!', 'Pokemon', 'Tokyo, Japan', '80000'))
    cursor.execute('INSERT INTO jobs (title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?)',
                    ('Racecar Driver', 'Driving is our passion', 'NASCAR', 'United States', '100000'))
    source.commit()
    api.jobsAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_jobs.txt")
    assert file_exists == True
    
def test_MyCollegeProfiles(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson'))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'Software Engineer', 'Computer Science', 'USF', 'I am well-versed in Python, C, C++, and Java, as well as Git', 'B.S.', '4'))
    cursor.execute('INSERT INTO profileJobs (fromUser, title, employer, location, dateStarted, dateEnded, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'Tech Associate', 'Best Buy', 'Tampa, Florida', '08/12/2018', '10/11/2021', 'I worked all round the store in assisting customer sales and aiding tech quality throughout the store'))
    source.commit()
    api.profilesAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_profiles.txt")
    assert file_exists == True
    
def test_MyCollegeUsers(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Homer3', 'Simpson12@', 'homer', 'simpson', 'plus'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Bart4', 'Simpson13@', 'bart', 'simpson', 'standard'))
    source.commit()
    api.usersAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_users.txt")
    assert file_exists == True

def test_MyCollegeTraining(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Homer3', 'Simpson12@', 'homer', 'simpson', 'plus'))
    cursor.execute('INSERT INTO coursesTaken (username, course) VALUES (?, ?);',
                   ('Homer3', 'Interview Training'))
    source.commit()
    api.trainingOutAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_training.txt")
    assert file_exists == True

def test_MyCollegeAppliedJobs(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Homer3', 'Simpson12@', 'homer', 'simpson', 'plus'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Bart4', 'Simpson13@', 'bart', 'simpson', 'standard'))
    cursor.execute('INSERT INTO jobs (jobID, poster, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?, ?);',
                   ('001', 'Homer3', 'Software Engineer', 'Code/debug', 'Google', 'California', '80000'))
    cursor.execute('INSERT INTO userJobRelation (username, jobID, status, reasoning) VALUES (?, ?, ?, ?);',
                   ('Bart4', '001', 'applied', 'I would like to work at a high-tier programming job'))
    source.commit()
    api.appliedJobsAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_appliedJobs.txt")
    assert file_exists == True

def test_MyCollegeSavedJobs(testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Homer3', 'Simpson12@', 'homer', 'simpson', 'plus'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('Bart4', 'Simpson13@', 'bart', 'simpson', 'standard'))
    cursor.execute('INSERT INTO jobs (jobID, poster, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?, ?);',
                   ('001', 'Homer3', 'Software Engineer', 'Code/debug', 'Google', 'California', '80000'))
    cursor.execute('INSERT INTO jobs (jobID, poster, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?, ?);',
                   ('002', 'Homer3', 'Pokemon Trainer', 'Catch Em All', 'Pokemon', 'Tokyo, Japan', '100000'))
    cursor.execute('INSERT INTO jobs (jobID, poster, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?, ?);',
                   ('003', 'Homer3', 'Cook', 'Cook food', 'McDonalds', 'Florida', '25000'))
    cursor.execute('INSERT INTO userJobRelation (username, jobID, status) VALUES (?, ?, ?);',
                   ('Bart4', '001', 'saved'))
    cursor.execute('INSERT INTO userJobRelation (username, jobID, status) VALUES (?, ?, ?);',
                   ('Bart4', '002', 'saved'))
    cursor.execute('INSERT INTO userJobRelation (username, jobID, status) VALUES (?, ?, ?);',
                   ('Bart4', '003', 'saved'))
    source.commit()
    api.savedJobsAPI("",cursor)

    file_exists = exists(API_OUTPUT_PATH + "MyCollege_savedJobs.txt")
    assert file_exists == True


def test_signUpAPI(testDB):
    cursor, source = testDB
    assert api.readFileIfExists("studentAccounts.txt")
    api.signUpAPI(source,cursor)
    cursor.execute("SELECT * FROM users WHERE username = 'homer'")
    queryResult = cursor.fetchone()
    expectedResults = ["homer","Simpson@12","homer","simpson"]
    for result in expectedResults:
        assert result in queryResult
    
