

#InCollege job management should be able to 
# delete a job, notify students job has been removed, 
# and next time they visit job section they get notified job has been deleted
import inCollege

def CheckJob(cursor, source, username, jobID):
    print(f"check job:'{jobID}'")
    cursor.execute(f"SELECT * FROM jobs WHERE jobID = '{jobID}'")
    job = cursor.fetchall()
    if not jobID:
        print("Job was deleted")
    else:
        print("job good")

def DeleteJob(cursor, source, username, jobID):
    #print("Delete jobs here")
    ID = jobID[0]
    print(f"Delete Job: '{ID}' ")
    cursor.execute(f"DELETE FROM jobs WHERE jobID = '{ID}' ")
    cursor.execute(f"DELETE FROM profileJobs WHERE jobID = '{ID}'")
    source.commit()
    inCollege.SearchJob(cursor, source, username)
    
    
#InCollege job management should be able to save job
# User: mark job as saved, genereate list of saved jobs 
# should be able to unmark saved jobs. THe list of saved jobs will be retained
# can be displayed next time they log in  
def SavedJob(cursor, source, username, jobID): 
    #print("Saved jobs here") 
    print(jobID)
    #Query the database with user and job id for userJobRelation
    # (FK Username, FK Jobid, status, grad_date, start, reasoning) PK Username, JobID
    print("Would you like to save a job (1), Unsave the job (2)")
    choice = input()
    if choice == '1':
        cursor.execute("INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, ?, ?, ?, ?);",
            (username, jobID, "saved", "NA", "NA", "NA"))
        source.commit()
    elif choice == '2':
        cursor.execute(f"DELETE FROM userJobRelation WHERE username = '{username}' AND jobID ='{jobID}' ")
        
        
