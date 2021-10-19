import sqlite3 as sql
from sys import argv

#creates a database called database.sqlite and inputs the user table
lnCollege = "database.sqlite" if len(argv) == 1 else argv[1]
source = sql.connect(lnCollege, timeout=10)

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
    language TEXT
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
# =============================================================================
# createOptionTable = """
# 
# CREATE TABLE options
# {
#      
#      email TEXT,
#      sms TEXT,
#      ad TEXT,
#      language TEXT
# };
# 
# """
# =============================================================================

cursor.execute(createTable)
cursor.execute(createJobTable)
cursor.execute(createProfileTable)
cursor.execute(createProfileJobsTable)
cursor.execute(createFriendTable)
cursor.execute(createUserJobRelation)
#cursor.execute(createOptionTable)
source.commit()

#INPUT ANY OTHER NECESSARY TABLE

source.close()
