

#InCollege job management should be able to 
# delete a job, notify students job has been removed, 
# and next time they visit job section they get notified job has been deleted
def DeleteJob(cursor, source, username, jobID):
    print("Delete jobs here")

#InCollege job management should be able to save job
# User: mark job as saved, genereate list of saved jobs
# should be able to unmark saved jobs. THe list of saved jobs will be retained
# can be displayed next time they log in  
def SavedJob(cursor, source, username, jobID): 
    print("Saved jobs here") 
    
    #Query the database with user and job id for userJobRelation
    # (FK Username, FK Jobid, status, grad_date, start, reasoning) PK Username, JobID
    print("Would you like to save a job (1), Change status of saved job (2)")
    choice = input()
    if choice == '1':
        cursor.execute("INSERT INTO userJobRelation (username, jobID, status, graduation_date, start_date, reasoning) VALUES (?, ?, ?, ?, ?, ?);",
            (username, jobID, "saved", "NA", "NA", "NA"))
    elif choice == '2':
        print("2") 
