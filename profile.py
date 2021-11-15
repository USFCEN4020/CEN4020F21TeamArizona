import inCollege
import profile

# Utility Lambda:

capitalizeWords = lambda words: " ".join([word.capitalize() for word in words.split()])


class Profile:
    def __init__(self,username,title=None,major=None,university=None,about=None,degree=None,yearsAtUni=None,experience=[]):
        self.username = username
        self.title = title
        self.major = capitalizeWords(major) if major else None
        self.university = capitalizeWords(university) if university else None
        self.about = about
        self.experience = experience
        self.degree = degree
        self.yearsAtUni = yearsAtUni

class ProfileJob:
    #The dateEnded and dateStarted parameters are strings in the format YYYY-MM-DD
    def __init__(self,title=None,employer=None, location=None, dateStarted=None,dateEnded=None,description=None):
        self.title = title
        self.employer = employer
        self.dateStarted = dateStarted
        self.dateEnded = dateEnded
        self.location = location
        self.description = description

#CRU API with the Database

def createProfile(cursor, connection, profile):
    with connection:
            query = """
                INSERT INTO profiles
                    (belongsTo, title, major, university, about, degree, yearsAtUni)
                    VALUES (?, ?, ?, ?, ?, ?, ?) 
                """
            values = (profile.username,profile.title,profile.major, profile.university,profile.about,profile.degree,profile.yearsAtUni)
            cursor.execute(query,values)
            for i, job in enumerate(profile.experience):
                query = """
                    INSERT INTO profileJobs
                        (jobID,fromUser,title,employer,location,dateStarted,dateEnded,description)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """
                values = (i,profile.username,job.title,job.employer,job.location,job.dateStarted,job.dateEnded,job.description)  
                cursor.execute(query,values)

def readProfile(cursor, username):
    cursor.execute(f"SELECT * FROM profiles WHERE belongsTo = '{username}'")
    profile = cursor.fetchone()
    cursor.execute(f"SELECT * FROM profileJobs WHERE fromUser = '{username}'")
    if profile:
        profileJobs = [ProfileJob(*job[2:]) for job in cursor.fetchall()]
        return Profile(*profile,profileJobs)
    return None

def updateProfile(cursor, connection, profile):
    with connection:
        query = f"""
            UPDATE profiles SET
                title='{profile.title}',
                major='{profile.major}',
                university='{profile.university}',
                about='{profile.about}',
                degree='{profile.degree}',
                yearsAtUni='{profile.yearsAtUni}'
            WHERE belongsTo='{profile.username}'
        """
        cursor.execute(query)
        for i,job in enumerate(profile.experience):
            query = f"""
                UPDATE profileJobs SET
                    title='{job.title}',
                    employer='{job.employer}',
                    location='{job.location}',
                    dateStarted='{job.dateStarted}',
                    dateEnded='{job.dateEnded}',
                    description='{job.description}'
                WHERE jobID={i} AND fromUser='{profile.username}'
            """
            cursor.execute(query)


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
        inCollege.Options(cursor, source, username)
        # inform user they don't have a profile and offer options to create or go back
    else:
        printProfile(result)
        print("Would you like to update your profile? type 'yes' to update it")

        choice = input()
        if choice.lower() == "yes":
            EditProfile(result, cursor)
            profile.updateProfile(cursor, source, result)
        inCollege.Options(cursor, source, username)


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