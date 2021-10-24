# Gabriel Gusmao de Almeida
# Tural Hagverdigev U10263909
# Antonio Gonzalez U57195076

# References:
# How to mock a single call to the bultin input() function with pytest - https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
# How to mock consecutive calls to input() with pytest - https://stackoverflow.com/questions/59986625/how-to-simulate-two-consecutive-console-inputs-with-pytest-monkeypatch
# How to read stdout with pytest - https://docs.pytest.org/en/6.2.x/capture.html

import inCollege
import sqlite3 as sql
import pytest
import profile
import connection 
import jobs
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
    cursor.execute(createTable)
    cursor.execute(createJobTable)
    cursor.execute(createProfileTable)
    cursor.execute(createProfileJobsTable)
    cursor.execute(createFriendTable)
    cursor.execute(createUserJobRelation)
    source.commit()
    return cursor, source


# Asserting that login fails when username does not exist
def test_FailedLogIn(monkeypatch, capsys, testDB):
    inputs = iter(['bart', 'simpson'])
    desiredOutput = 'user does not exist with this username and password combination\n'
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, _ = testDB
    try:
        inCollege.logIn(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# Asserting that sign ups with weak passwords won't be allowed
def test_WeakPasswords(monkeypatch, capsys, testDB):
    tests = [iter(['bart', 'simpson']), iter(['bart', 'Simpson']), iter(['bart', 'Simpson1']),
             iter(['bart', 'Simpson@']), iter(['bart', 'simpson12@'])]
    desiredOutput = "Invalid option. Password must between 8 and 12 characters, have a digit, capital letter, and a special character\n"
    cursor, source = testDB
    for inputs in tests:
        monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
        try:
            inCollege.signUp(cursor, source)
        except(StopIteration):
            output = capsys.readouterr().out
            assert output == desiredOutput

# Asserting successful sign up when the password is strong enough
def test_ValidSignUp(monkeypatch, capsys, testDB):
    inputs = iter(['bart', 'Simpson12@', 'Bart', 'Simpson'])
    desiredOutput = 'Logged in!\n'
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.signUp(cursor, source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# Asserting that sign ups where the username already exists will fail
def test_UsernameExistsInSignUp(monkeypatch, capsys, testDB):
    inputs = iter(['bart'])
    desiredOutput = 'Username already exists\n'
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('bart', 'Simpson@12', 'bart', 'simpson'))
    source.commit()

    try:
        inCollege.signUp(cursor, source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# Asserting successful login when account is in database
def test_SuccessfullLogin(monkeypatch, capsys, testDB):
    inputs = iter(['bart', 'Simpson12@'])
    desiredOutput = 'Logged in!\n'
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('bart', 'Simpson12@', 'bart', 'simpson'))
    source.commit()
    try:
        inCollege.logIn(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_MaxAccounts(monkeypatch, capsys, testDB):
    tests = [iter(['bart', 'Simpson12@', 'Bart', 'Simpson']), iter(['marge', 'Simpson12@', 'Marge', 'Simpson']),
             iter(['homer', 'Simpson12@', 'Homer', 'Simpson']), iter(['maggie', 'Simpson12@', 'Maggie', 'Simpson']),
             iter(['lisa', 'Simpson12@', 'Lisa', 'Simpson']), iter(['mrburns', 'Simpson12@', 'Mr.', 'Burns'])]
    desiredOutput = "Unable to sign up. There is already the maximum number of users.\n"
    cursor, source = testDB
    for inputs in tests:
        monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
        try:
            inCollege.signUp(cursor, source)
        except(StopIteration):
            output = capsys.readouterr().out
            assert output == desiredOutput

# Asserting that 5 skills show up after logged in and skills option is selected
def test_SkillsAreDisplaying(monkeypatch, capsys, testDB):
    inputs = iter(["learn skill"])
    desiredOutput = "Select Option\n=======================================================================================================================================================================\n______________________________________________________________\nC++ | Java | Python | SQL | JavaScript | No Selection\n______________________________________________________________\n"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.Options(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# Assert that if a existing user is found when searched
def test_SearchExistingUserWhileSignedIn(monkeypatch, capsys, testDB):
    inputs = iter(["homer", "simpson"])
    desiredOutput = "They are a part of the InCollege system\nSearch again: 0\n"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson'))
    source.commit()
    try:
        inCollege.FindPerson1(cursor, "",source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


# Assert that if a non existing user is not found when searched
def test_SearchNonExistingUser(monkeypatch, capsys, testDB):
    inputs = iter(['Mr.', 'Burns'])
    desiredOutput = "They are not yet a part of the InCollege system\nSearch again: 0\n"
    cursor, source = testDB
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.FindPerson1(cursor, "",source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_video(monkeypatch, capsys,testDB):
    inputs = iter(['1', ])
    desiredOutput = "Video is now playing\n\nThanks to inCollege I was able to meet with fellow college students and establish connections\nthat allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege\nI was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft\n--Alyssa (Arizona)\nWould you like to sign in or sign up? 0 for sign in, and 1 for sign up: \n3 for information video | Search Person 4\n5 for Useful Links | 6 for InCollege Important Links\n"
    cursor, source = testDB
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.PlayVideo(cursor,source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_userSuccessStory(capsys):
    desiredOutput = "Thanks to inCollege I was able to meet with fellow college students and establish connections\nthat allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege\nI was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft\n--Alyssa (Arizona)\n"
    inCollege.successStory()
    output = capsys.readouterr().out
    assert output == desiredOutput


def test_searchExistingUserWhileLoggedOut(monkeypatch, capsys, testDB):
    desiredOutput = "They are a part of the InCollege system\nWould like to join them and sign up? Press 1\n"
    cursor, source= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson'))
    source.commit()
    inputs = iter(['homer', 'simpson'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.FindPerson(cursor,source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_searchNonExistingUserWhileLoggedOut(monkeypatch, capsys, testDB):
    desiredOutput = "They are not yet a part of the InCollege system\nSearch again: 0\n"
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson'))
    source.commit()
    inputs = iter(['homer', 'jackson'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.FindPerson(cursor,source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_postingJob(monkeypatch, capsys, testDB):
    desiredOuput = 'Posting job now\nTo post another job, press 1:\n'
    inputs = iter(
        ['yes', 'Nuclear Safety Inspector', 'Inspect Saftety of Nuclear Power Plant (in Sector 7-G)', 'Mr. Burns',
         'Springfield', '37k'])
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('mrburns', 'Simpson12@', 'montegomery', 'burns'))
    source.commit()
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.SearchJob(cursor, source, "mrburns")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOuput

def test_InCollegeLink1(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nCopyright 2021 InCollege USA. All rights reserved.\n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['1', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB

    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_InCollegeLink2(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nAn Encouraging online platform for College Students\n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['2', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB

    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_InCollegeLink3(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nAs part of our commitment to accessibility we continuously audit our products—internally using assistive technology like screen reading software.\n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['3', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_InCollegeLink4(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nPlease read this Mobile Application End User License Agreement (“EULA”) carefully before downloading or using the InCollege Inc.\n(“InCollege”) application (“Mobile App”), which allows You to access InCollege’s internet-delivered service (“Subscription Service”)\n from Your mobile device. This EULA forms a binding legal agreement between you (and any other entity on whose behalf you accept these terms)\n (collectively “You” or “Your”) and InCollege (each separately a “Party” and collectively the “Parties”) as of the date you download the Mobile App. \nYour use of the Mobile App is subject to this EULA and Your use of the Subscription Service will remain subject to the existing agreement governing such use (the “Subscription Agreement”). \nWith respect to the use of the Mobile App, and to the extent the Subscription Agreement conflicts with this EULA, the terms of this EULA will govern and control solely with respect to use of the Mobile App. \n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['4', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_EmailNotifChange(monkeypatch, capsys, testDB):
    desiredOutput = "InCollege (“we” or “us” or “our”) respects the privacy of our users (“user” or “you”). \nThis Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our mobile application (the “Application”).\nPlease read this Privacy Policy carefully. IF YOU DO NOT AGREE WITH THE TERMS OF THIS PRIVACY POLICY, PLEASE DO NOT ACCESS THE APPLICATION.\nWe reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the “Last updated” date of this Privacy Policy.\nYou are encouraged to periodically review this Privacy Policy to stay informed of updates. You will be deemed to have been made aware of, will be subject to, and will be deemed to have accepted the changes in any revised Privacy Policy\n by your continued use of the Application after the date such revised Privacy Policy is posted.\n\nInCollege email turned off"
    inputs = iter(['1', "off"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB;
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', 'Spanish'))
    source.commit()
    try:
        inCollege.GuestControls(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_SMSchange(monkeypatch, capsys, testDB):
    desiredOutput = "InCollege (“we” or “us” or “our”) respects the privacy of our users (“user” or “you”). \nThis Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our mobile application (the “Application”).\nPlease read this Privacy Policy carefully. IF YOU DO NOT AGREE WITH THE TERMS OF THIS PRIVACY POLICY, PLEASE DO NOT ACCESS THE APPLICATION.\nWe reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the “Last updated” date of this Privacy Policy.\nYou are encouraged to periodically review this Privacy Policy to stay informed of updates. You will be deemed to have been made aware of, will be subject to, and will be deemed to have accepted the changes in any revised Privacy Policy\n by your continued use of the Application after the date such revised Privacy Policy is posted.\n\nSMS turned on"
    inputs = iter(['2', "on"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB;
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', 'Spanish'))
    source.commit()
    try:
        inCollege.GuestControls(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_AdChange(monkeypatch, capsys, testDB):
    desiredOutput = "InCollege (“we” or “us” or “our”) respects the privacy of our users (“user” or “you”). \nThis Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our mobile application (the “Application”).\nPlease read this Privacy Policy carefully. IF YOU DO NOT AGREE WITH THE TERMS OF THIS PRIVACY POLICY, PLEASE DO NOT ACCESS THE APPLICATION.\nWe reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the “Last updated” date of this Privacy Policy.\nYou are encouraged to periodically review this Privacy Policy to stay informed of updates. You will be deemed to have been made aware of, will be subject to, and will be deemed to have accepted the changes in any revised Privacy Policy\n by your continued use of the Application after the date such revised Privacy Policy is posted.\n\nTargeted advertising turned off"
    inputs = iter(['3', "off"])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB;
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', 'Spanish'))
    source.commit()
    try:
        inCollege.GuestControls(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_InCollegeLink6(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nPerformance cookies: these types of cookies recognise and count the number of visitors to a website and users of an App and to see how users move around \nin each. This information is used to improve the way the website and App work.\nFunctionality cookies: these cookies recognise when you return to a website or App, enable personalised content and recognise and remember your preferences.\n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['6', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_InCollegeLink7(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nYou can't post someone else’s private or confidential information without permission or do anything that\nviolates someone else's rights, including intellectual property rights (e.g., copyright infringement, trademark infringement, counterfeit, or pirated goods).\n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['7', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_InCollegeLink8(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nThis policy governs the use of all InCollege trademarks for any purpose and applies to the entire InCollege system. Consistency\nin the use of Incollege trademarks strengthens their value and our ability to protect them from unauthorized use. \n\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['8', ])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_InCollegeLink9(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nSpanish\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['9', 'Spanish'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson'))
    source.commit()
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_InCollegeLink9WithSpanish(monkeypatch, capsys, testDB):
    desiredOutput = "Copyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\nEnglish\nCopyright Notice (1), About (2), Accessibility (3)\nUser Agreement (4), Privacy Policy (5), Cookie Policy (6)\nCopyright Policy (7), Brand Policy (8), Languages (9)\n"
    inputs = iter(['9', 'English'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?);',
                   ('homer', 'Simpson12@', 'homer', 'simpson', 'Spanish'))
    source.commit()
    try:
        inCollege.InCollegeLink(cursor, source, "homer")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


# Asserting successful after testing useful links
def test_general(monkeypatch, capsys):
    inputs = iter(["2","3","4"])
    desiredOutput = "Under construction"
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.UsefulLink("")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

#function works but does not account for input question
def test_ViewProfile(monkeypatch, capsys, testDB):
    inputs = iter(["n"])

    #accounts for last line of output not used atm
    end_statement = "Would you like to update your profile? type 'yes' to update it"
    
    #iterates through inputs not used atm 
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    
    #connects to database and adds profilej for homer
    cursor, source = testDB
    cursor.execute("INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?);",
                   ('homer', 'Homer Simpson', 'Computer Science', 'Su', 'N/a', 'Bs', 4))
    
    #reads profile and checks the printed function to the expected
    #output
    prof = profile.readProfile(cursor, 'homer')
    out = inCollege.printProfile(prof)
    desiredOutput = str(out)
    try:
        #since we just care about the printing of the menu test using the printProfile function 
        inCollege.printProfile(prof)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
        

#must be able to edit profile/ update profile
def test_EditProfile(monkeypatch, capsys, testDB):
    #inputs to answer for editing the profile
    inputs = iter(['n', 'yes', 'Computer Science', 'n', 'n', 'n', 'n', 'n'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    #insert homer into testDB
    source,cursor = testDB 
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'Engineer', 'Physics', 'Su', 'N/a', 'Bs', 4))
    
    homer = profile.readProfile(source, 'homer')
    #make profile to check to make sure edits are valid
    prof = profile.Profile('homer', 'Engineer', 'Computer Science', 'Su', 'Na', 'Bs', 4)
    out = inCollege.printProfile(prof)
    desiredOutput = str(out)
    
    try:
       inCollege.EditProfile(homer,"")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
        

#must be able to partially put in profile information 
def test_TryPartial(monkeypatch, capsys, testDB):
    inputs = iter(['yes','yes','Homer','n','n','n','n', 'n'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    #make homer user
    source,cursor = testDB
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'None', 'None', 'None', 'None', 'None', 4))

    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('Homer', 'None', 'None', 'None', 'None', 'None', 4))
    #homer profile to check output against Homer
    homer = profile.readProfile(source, 'homer')
    prof =  profile.readProfile(source, 'Homer')
    out = inCollege.printProfile(prof)
    desiredOutput = str(out)

    try:
        #edit homer information, change homer -> Homer and leave rest partial
        #monkeypatch uses "" to pass input to functions
        inCollege.EditProfile(homer,"")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    
# Must be able to enter the necessary profile info
def test_ProfileInfo(monkeypatch, capsys, testDB):
    inputs = iter(['yes', 'yes', 'Homer', 'yes', 'Physics', 'yes', 'Su', 'Im homer simpson', 'n'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?)',
                    ('homer', 'Simpson12@', 'homer', 'simpson', 'English'))
    source.commit()

    try:
        inCollege.inProfile(cursor, source, 'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output

# Must be able to enter text into the About section for a profile
def test_AboutInfo(monkeypatch, capsys, testDB):
    inputs = iter(['yes', 'yes', 'Bart', 'yes', 'Computer Science', 'yes', 'Bs', 'According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees do not care what humans think impossible.', 'n'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?)',
                    ('bart', 'Simpson13*', 'bart', 'simpson', 'English'))
    source.commit()

    try:
        inCollege.inProfile(cursor, source, 'bart')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output

# Must be able to enter information for the Education section in a profile
def test_EducationInfo(monkeypatch, capsys, testDB):
    inputs = iter(['yes', 'yes', 'Bob', 'yes', 'Computer Science', 'yes', 'Bs', 'There is nothing about me', 'n',
                   'n', 'yes', 'Bachelors', 'yes', '3'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?)',
                    ('Bob', 'Bobby123*', 'bob', 'ross', 'English'))
    source.commit()

    try:
        inCollege.inProfile(cursor, source, 'Bob')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output

# Must convert the major and university to have the first letter be uppercase for each word
def test_NameConv(monkeypatch, capsys, testDB):
    inputs = iter(['yes', 'yes', 'Ash', 'yes', 'zoology', 'yes', 'kanto university', 'n'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?)',
                    ('Ash', 'Iamten10@', 'ash', 'ketchum', 'English'))
    source.commit()

    try:
        inCollege.inProfile(cursor, source, 'Ash')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output

# Must be able to enter up to 3 previous jobs for a profile
def test_Experience(monkeypatch, capsys, testDB):
    inputs = iter(['yes', 'yes', 'John', 'yes', 'aerospace engineering', 'yes', 'UF', 'yes',
                   'I am currently seeking employment in the field of aerospace engineering', 'yes',
                   iter(['Cashier', 'Dunkin Donuts', 'Orlando', '5/29/2016', '6/12/2018', 'I worked the register and occasionally ate donuts']), 'yes',
                   iter(['Cashier', '7-11', 'Orlando', '7/11/2018', '7/11/2019', 'I worked the register and occasionally drank slushies']), 'yes',
                   iter(['Engineering Intern', 'NASA', 'Ft. Lauderdale', '4/20/2020', '10/15/2020', 'I assisted on the development of rockets']), 'no'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))

    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName, language) VALUES (?, ?, ?, ?, ?)',
                    ('John', 'johN456*', 'john', 'smith', 'English'))
    source.commit()

    try:
        inCollege.inProfile(cursor, source, 'John')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output

# Test the new maximum number of student accounts that can be created
def test_NewMaxAccounts(monkeypatch, capsys, testDB):
    tests = [iter(['burt', 'Simpson12@', 'Burt', 'Simpson']), iter(['murge', 'Simpson13@', 'Murge', 'Simpson']),
             iter(['humer', 'Simpson14@', 'Humer', 'Simpson']), iter(['muggie', 'Simpson15@', 'Muggie', 'Simpson']),
             iter(['lusa', 'Simpson16@', 'Lusa', 'Simpson']), iter(['msburns', 'Simpson17@', 'Ms.', 'Burns']),
             iter(['bob', 'Bobby123@', 'Bob', 'Ross']),
             iter(['ash', 'Iamten10@', 'Ash', 'Ketchum']),
             iter(['john', 'Noobmaster6@', 'John', 'Smith']), 
             iter(['jane', 'Jane365@@', 'Jane', 'Doe']),
             iter(['peter', 'Spiderman1@', 'Peter', 'Parker'])]
    desiredOutput = "Unable to sign up. There is already the maximum number of users.\n"
    cursor, source = testDB
    for inputs in tests:
        monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
        try:
            inCollege.signUp(cursor, source)
        except(StopIteration):
            output = capsys.readouterr().out
            assert output == desiredOutput

# List of friends on inCollege will initially be empty
def test_FriendsListEmpty(monkeypatch, capsys, testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('Homer1', 'Simpson11@', 'Homer', 'Simpson'))
    conn = connection.getConnections(cursor, source, 'Homer1')
    desiredOutput = len(conn)
    assert desiredOutput == 0

# User will have a list of friends on InCollege that they have connected with
def test_FriendsOnInCollege(monkeypatch, capsys, testDB):
    inputs = iter(['n',])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('Homer1', 'Simpson11@', 'Homer', 'Simpson'))
    cursor.execute('INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, ?)',
                    ('homer', 'bart', 'friend'))
    conn = connection.getConnections(cursor, source, 'homer')
    desiredOutput = str(conn)
    assert desiredOutput != 0

# User will be able to send a friend request by searching for a last name, university, or major
def test_MakeFriend(monkeypatch, capsys, testDB):
    desiredOutput = "Friend Request Sent\nSelect Option\n=======================================================================================================================================================================\n"
    inputs = iter(['Simpson', '0', '0', '0'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('homer', 'Simpson12@', 'Homer', 'Simpson'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('bart', 'Simpson13@', 'Bart', 'Simpson'))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('bart', 'Engineer', 'Physics', 'Su', 'N/a', 'Bs', 4))
    source.commit()

    try:
        inCollege.MakeFriend(cursor, source, 'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        print(output)
        assert output == desiredOutput
    
# User will be able to view incoming friend requests and accept them
def test_AcceptFriendRequest(monkeypatch, capsys, testDB):
    desiredOutput = "Select Option\n=======================================================================================================================================================================\nSelect Option\n=======================================================================================================================================================================\n"
    inputs = iter(['0', '0', '0'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('homer', 'Simpson12@', 'Homer', 'Simpson'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('bart', 'Simpson13@', 'Bart', 'Simpson'))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'Pilot', 'Aviation', 'Ny', 'N/a', 'Ms', 3))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('bart', 'Engineer', 'Physics', 'Su', 'N/a', 'Bs', 4))
    cursor.execute('INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, ?)',
                    ('homer', 'bart', 'pending'))
    source.commit()

    try:
        inCollege.ViewFriendRequest(cursor, source, 'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

# User will be able to view incoming friend requests and reject them
def test_RejectFriendRequest(monkeypatch, capsys, testDB):
    desiredOutput = ""
    inputs = iter(['0', '1', '0'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('homer', 'Simpson12@', 'Homer', 'Simpson'))
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                    ('bart', 'Simpson13@', 'Bart', 'Simpson'))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('homer', 'Pilot', 'Aviation', 'Ny', 'N/a', 'Ms', 3))
    cursor.execute('INSERT INTO profiles (belongsTo, title, major, university, about, degree, yearsAtUni) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    ('bart', 'Engineer', 'Physics', 'Su', 'N/a', 'Bs', 4))
    cursor.execute('INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, ?)',
                    ('homer', 'bart', 'pending'))
    source.commit()

    try:
        inCollege.ViewFriendRequest(cursor, source, 'homer')
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput


def test_JobPostingMax(monkeypatch, capsys, testDB):
    desiredOutput = "Unable to add job. There is already the maximum number of jobs posted.\n"
    cursor, source = testDB
    with capsys.disabled():
        inputs = iter((["yes"] + ["soul power" for _ in range(5)] + ["1"]) * 10)
        monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
        cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                        ('tommorello', 'Morello12@', 'Tom', 'Morello'))
        try:
            inCollege.SearchJob(cursor,source,"tommorello")
        except: pass
    inputs = iter((["yes"] + ["soul power" for _ in range(5)] + ["1"]))
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
            inCollege.SearchJob(cursor,source,"tommorello")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_DeleteJob(monkeypatch, testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO jobs (jobID, poster, title) VALUES (?, ?, ?)',
                    (0,'tommorello', 'Sound Engineer'))
    inputs = iter(['remove','Sound Engineer'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.SearchJob(cursor,source,"tommorello")
    except(StopIteration):
        cursor.execute("SELECT * FROM jobs WHERE jobID = 0")
        result = cursor.fetchall()
        assert len(result) == 0

def test_applyForJob(monkeypatch, capsys, testDB):
    desiredOutput = "Successfully applied!\nSelect Option\n=======================================================================================================================================================================\n"
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)',
                        ('tommorello', 'Morello12@', 'Tom', 'Morello'))
    cursor.execute('INSERT INTO jobs (jobID, poster, title) VALUES (?, ?, ?)',
                    (0,'tommorello', 'Sound Engineer'))
    inputs = iter(['07/01/2022', '08/01/2022', 'i need a job'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        inCollege.applyForJob(cursor, source, "tommorello",0)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_SaveJob(monkeypatch, capsys, testDB):
    cursor, source = testDB
    cursor.execute('INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, ?, ?, ?, ?)',
                    ('tommorello',0,'saved','07/01/2022','08/01/2022', 'i need a job'))
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    try:
        jobs.SavedJob(cursor,source,"tommorello",1)
    except(StopIteration):
        cursor.execute("SELECT * FROM userJobRelation WHERE status = saved")
        result = cursor.fetchall()
        assert len(result) == 0