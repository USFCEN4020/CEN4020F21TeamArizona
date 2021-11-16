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
        dateStarted TEXT,
        dateEnded TEXT,
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
cursor.execute(createMessages)
cursor.execute(createNotifications)
cursor.execute(createCoursesTaken)
cursor.execute(createTraining)
initialTrainings = ["Training and Education","Help Desk","Business Analysis and Strategy","Security"]
for training in initialTrainings:
    cursor.execute(f"INSERT INTO trainings(title) VALUES('{training}')")
#cursor.execute(createOptionTable)
source.commit()

#INPUT ANY OTHER NECESSARY TABLE

source.close()
