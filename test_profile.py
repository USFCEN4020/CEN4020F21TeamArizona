import profile
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

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
    title TEXT,
    description TEXT,
    employer TEXT,
    location TEXT,
    salary INTEGER,
    first TEXT,
    last TEXT
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

    )

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
with connection:
    cursor.execute(createTable)
    cursor.execute(createJobTable)
    cursor.execute(createProfileTable)
    cursor.execute(createProfileJobsTable)


def assertProfilesAreEqual(profile1,profile2):
    for key in profile2.__dict__:
        newAttrs = profile1.__dict__
        readAttrs = profile2.__dict__
        if key != 'experience':
            assert newAttrs[key] == readAttrs[key]
        else:
            for i in range(len(newAttrs[key])):
                for inner_key in newAttrs[key][i].__dict__:
                    assert readAttrs[key][i].__dict__[inner_key] == newAttrs[key][i].__dict__[inner_key]

def test_createReadProfile():
    job = profile.ProfileJob("Nuclear Safety Inspector","Mr. Burns","1970-01-01","2021-10-07","Springfield","Eating Donuts")
    newProfile = profile.Profile("homer","Homer Simpson","Nuclear Physics","SU","Starred in Famous TVSHOW","BS",1,[job])
    profile.createProfile(cursor,connection,newProfile)
    readProfile = profile.readProfile(cursor,newProfile.username)
    assertProfilesAreEqual(newProfile,readProfile)
    


def test_updateProfile():
    jobUpdate = profile.ProfileJob("Nuclear Safety Inspector","Mr. Burns","1970-01-01","2021-10-07","Springfield","I mean... I do actual work")
    profileUpdate = profile.Profile("homer","Homer Simpson","Astronaut","None","Went to space","None",0,[jobUpdate])
    profile.updateProfile(cursor,connection,profileUpdate)
    readProfile = profile.readProfile(cursor,profileUpdate.username)
    assertProfilesAreEqual(profileUpdate,readProfile)