#all data will be stored in mysql database
#go to mysql CLI and create databse "assgn_tracker"
   #USE assgn_tracker;

import mysql.connector as connector
from dbconfig import dbconfig  #for connection

#create connection
con = connector.connect(host=dbconfig['host'], port=dbconfig['port'], user=dbconfig['username'], password=dbconfig['password'], database='pytest')
#cursor for this connection
cursor = con.cursor()

#table
#create a new table for each user
#assgn  subject  due  progress  
def create_table() :
    #the table to store data abt assignements
    query = "CREATE TABLE IF NOT EXISTS tbl(assgn VARCHAR(100), subject VARCHAR(80), due DATE , progress VARCHAR(20)) ;"
    cursor.execute(query)



#functions
#insert task function
def add_assgn(assgn , progress , due, subject) :
    query = "INSERT INTO tbl VALUES (%s, %s , %s , %s) ;"
    # %s = string input
    # date is also being treated as string???

    cursor.execute(query, (assgn,subject,due,progress) )
    con.commit()

#doesnt matter if there are multiple entries of the same subject due to
#multiple assgns of the same subject
#when an assgn is deleted, one entry of that subj will be deleted
#so when there are no active assgn of that subject, the subject will be automatically deleted


#remove subject entry
#when assgn is deleted
def remove_sub_entry(subject) :
    query = 'DELETE FROM sub_tbl WHERE subject=(%s) ;'
    cursor.execute(query, (subject))
    con.commit()



#getting list of subjects
def get_sub_list() :
    #list of subjects
    list = ["All"]

    query = 'SELECT DISTINCT subject FROM tbl ;'
    cursor.execute(query)

    #now cursor has all the data
    #accesses each value in the given column (col) of the data stored in cursor
    for row in cursor :
        sub = row[0]
        list.append(sub)

    return list


def display_all() :
    query = "SELECT * FROM tbl ORDER BY due ASC;"
    cursor.execute(query)

    #now cursor has all the tasks
    data = cursor.fetchall()

    #now "data" has all the assignments
    return data


def display_subject_tasks( subject ) :
    query = "SELECT * FROM tbl WHERE subject='{}' ORDER BY due ASC ;".format(subject)

    cursor.execute(query)

    #now cursor has all the tasks
    data = cursor.fetchall()

    #now "data" has all the assignments
    return data


def get_assignment_list():
    #list of subjects
    list = []

    query = 'SELECT assgn FROM tbl ;'
    cursor.execute(query)

    #now cursor has all the data
    for row in cursor :
        sub = row[0]
        list.append(sub)

    return list



#edit the assignment
def edit_assgn(old_assgn,  new_progress , new_due) :
    query = "UPDATE tbl SET due='{}', progress='{}' WHERE assgn='{}' ;".format( new_due, new_progress, old_assgn)

    cursor.execute(query )
    con.commit()


#delete assignment
def delete_assignment(assgn) :
    query = "DELETE FROM tbl WHERE assgn='{}' ;".format(assgn)

    cursor.execute(query )
    con.commit()


#delete all assignments
def clear() :
    query = "TRUNCATE TABLE tbl ;"

    cursor.execute(query )
    con.commit()

#pie charts
#subject
def subject_data() :
    query = "SELECT subject, COUNT(*) FROM tbl GROUP BY subject ;"
    cursor.execute(query)

    #organise data into 2 lists
    # sub[i] = ith subject
    #count[i] = # of assignments of ith subject
    
    sub = []
    count = []
    i = 0

    for row in cursor :
        s = row[0]
        c = row[1]
        sub.append(s)
        count.append(c)


    return sub, count


#subject
def progress_data() :
    query = "SELECT progress, COUNT(*) FROM tbl WHERE progress != 'Done' GROUP BY progress ;"
    cursor.execute(query)

    #organise data into 2 lists
    # sub[i] = ith subject
    #count[i] = # of assignments of ith subject
    
    prog = []
    count = []
    i = 0

    for row in cursor :
        p = row[0]
        c = row[1]
        prog.append(p)
        count.append(c)


    return prog, count







