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
