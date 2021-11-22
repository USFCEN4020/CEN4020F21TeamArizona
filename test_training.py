import inCollege
import sqlite3 as sql
import pytest
import profile
import connection 
import jobs
import message
import learning
from message import Messages
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
    cursor.execute(createTraining)
    initialTrainings = ["Training and Education","Help Desk","Business Analysis and Strategy","Security"]
    for training in initialTrainings:
        cursor.execute(f"INSERT INTO trainings(title) VALUES('{training}')")
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


def test_listOfAvailableCourses(monkeypatch, capsys, testDB):
    desiredOutput = "-----------------------------------------------------\nYou can press B to go back to the main menu\nHere are the current available courses:\n-----------------------------------------------------\nHow to use In College learning | to select this course press 0\n\nGamification of learning | to select this course press 1\n\nTrain the Trainer | to select this course press 2\n\nUnderstanding the Architectural Design Process | to select this course press 3\n\nProject Management Simplified | to select this course press 4\n\n"
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', '1'))
    source.commit()
    inputs = iter(['B'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        learning.Learning(cursor,source,'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_CompletedTraining(monkeypatch, capsys, testDB):
    desiredOutput = "Course completed!\n-----------------------------------------------------\nYou can press B to go back to the main menu\nHere are the current available courses:\n-----------------------------------------------------\nHow to use In College learning | to select this course press 0 | Done\n\nGamification of learning | to select this course press 1\n\nTrain the Trainer | to select this course press 2\n\nUnderstanding the Architectural Design Process | to select this course press 3\n\nProject Management Simplified | to select this course press 4\n\n"
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', '1'))
    source.commit()
    inputs = iter(['0', 'B'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        learning.Learning(cursor,source,'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_TakeCompletedTrainingAgain(monkeypatch, capsys, testDB):
    desiredOutput = "You have now completed this training\n-----------------------------------------------------\nYou can press B to go back to the main menu\nHere are the current available courses:\n-----------------------------------------------------\nHow to use In College learning | to select this course press 0 | Done\n\nGamification of learning | to select this course press 1\n\nTrain the Trainer | to select this course press 2\n\nUnderstanding the Architectural Design Process | to select this course press 3\n\nProject Management Simplified | to select this course press 4\n\n"
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', '1'))
    source.commit()
    inputs = iter(['0', 'B', '0', 'B'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        learning.Learning(cursor,source,'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_CancelTraining(monkeypatch, capsys, testDB):
    desiredOutput = "Course Cancelled\n-----------------------------------------------------\nYou can press B to go back to the main menu\nHere are the current available courses:\n-----------------------------------------------------\nHow to use In College learning | to select this course press 0 | Done\n\nGamification of learning | to select this course press 1\n\nTrain the Trainer | to select this course press 2\n\nUnderstanding the Architectural Design Process | to select this course press 3\n\nProject Management Simplified | to select this course press 4\n\n"
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, membershipType) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', '1'))
    source.commit()
    inputs = iter(['0', 'B', '0', 'B'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        learning.Learning(cursor,source,'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# Test four training options - Result "Under Construction"
# IT help desk or security - "Coming soon"
# Business Analysis & Strategy - "Present few options"
# Business Analysis & Strategy - "Present sign in after selecting option"
def test_Training(monkeypatch,capsys,testDB):
    inputs = iter(['7', '0', '0'])
    cursor, _ = testDB
    desiredOutput = "Under Construction"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.trainingProgram(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_IT(monkeypatch, capsys,testDB): 
    inputs = iter(['7','1'])
    cursor, _ = testDB
    desiredOutput = "Coming Soon!"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.trainingProgram(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_Toptions(monkeypatch,capsys,testDB):
    inputs = iter(['7'])
    cursor, _ = testDB
    desiredOutput = "Please choose one of the options you would like\n0 for Training and Education | 1 for IT Help Desk | 2 for Business Analysis and Strategy | 3 for Security"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.trainingProgram(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_BnA(monkeypatch,capsys,testDB):
    inputs = iter(['7','2'])
    cursor,_ = testDB
    desiredOutput = "Please choose one of the options\n 0 for How to use inCollege Learning, 1 for Train the trainer, 2 for Gamification of learning, 3 for else"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.trainingProgram(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_BnA1(monkeypatch,capsys,testDB):
    cursor, _ = testDB
    inputs = iter(['7','2','1'])
    desiredOutput = "Please choose one of the options\n 0 for How to use inCollege Learning, 1 for Train the trainer, 2 for Gamification of learning, 3 for else\nPlease choose sign in from the menu and sign into see the rest of the results"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.trainingProgram(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput