#all data will be stored in mysql database
#go to mysql CLI and create databse "assgn_tracker"
   #USE assgn_tracker;

import mysql.connector as connector
from dbconfig import dbconfig  #for connection
    

#create connection
con = connector.connect(host=dbconfig['host'], port=dbconfig['port'], user=dbconfig['username'], password=dbconfig['password'], database='assgn_tracker')
#cursor for this connection
cursor = con.cursor()

##########################################################################################################
#for log in and authentication

#table = "users"
#col: email , password

#get dictionary of users
def getUsers() :
    dict = {}

    query = 'SELECT * FROM users ;'
    cursor.execute(query)

    #add each entry to the dict
    for row in cursor :
        email = row[0]
        pw = row[1]

        # dict[key] = value
        dict[email] = pw

    return dict


#separate table for each user
#table name = email address of user

#assgn  subject  due  progress  

#create new table for new user table 
def create_table( tbl_name) :
    #the table to store data abt assignements
    query = "CREATE TABLE IF NOT EXISTS `{}`(assgn VARCHAR(100), subject VARCHAR(80), due DATE , progress VARCHAR(20)) ;".format(tbl_name)
    cursor.execute(query)
    con.commit()


#add new user
#add credentials of new user to user table
def addUser(email, passw) :
    query = "INSERT INTO users VALUES (%s, %s) ;"

    cursor.execute(query, (email, passw) )
    con.commit()



##########################################################################################################






#functions
#insert task function
def add_assgn(tbl, assgn , progress , due, subject) :
    query = "INSERT INTO `{}` VALUES (%s, %s , %s , %s) ;".format(tbl)
    # %s = string input
    # date is also being treated as string???

    cursor.execute(query, (assgn,subject,due,progress) )
    con.commit()

#doesnt matter if there are multiple entries of the same subject due to
#multiple assgns of the same subject
#when an assgn is deleted, one entry of that subj will be deleted
#so when there are no active assgn of that subject, the subject will be automatically deleted



#getting list of subjects
def get_sub_list(tbl) :
    #list of subjects
    list = ["All"]

    query = 'SELECT DISTINCT subject FROM `{}` ;'.format(tbl)
    cursor.execute(query)

    #now cursor has all the data
    #accesses each value in the given column (col) of the data stored in cursor
    for row in cursor :
        sub = row[0]
        list.append(sub)

    return list


def display_all(tbl) :
    query = "SELECT * FROM `{}` ORDER BY due ASC;".format(tbl)
    cursor.execute(query)

    #now cursor has all the tasks
    data = cursor.fetchall()

    #now "data" has all the assignments
    return data


def display_subject_tasks( tbl, subject ) :
    query = "SELECT * FROM `{}` WHERE subject='{}' ORDER BY due ASC ;".format(tbl, subject)

    cursor.execute(query)

    #now cursor has all the tasks
    data = cursor.fetchall()

    #now "data" has all the assignments
    return data


def get_assignment_list(tbl):
    #list of subjects
    list = []

    query = 'SELECT assgn FROM `{}` ;'.format(tbl)
    cursor.execute(query)

    #now cursor has all the data
    for row in cursor :
        sub = row[0]
        list.append(sub)

    return list



#edit the assignment
def edit_assgn(tbl, old_assgn,  new_progress , new_due) :
    query = "UPDATE `{}` SET due='{}', progress='{}' WHERE assgn='{}' ;".format( tbl, new_due, new_progress, old_assgn)

    cursor.execute(query )
    con.commit()


#delete assignment
def delete_assignment(tbl, assgn) :
    query = "DELETE FROM `{}` WHERE assgn='{}' ;".format(tbl, assgn)

    cursor.execute(query )
    con.commit()


#delete all assignments
def clear(tbl) :
    query = "TRUNCATE TABLE `{}` ;".format(tbl)

    cursor.execute(query )
    con.commit()

#pie charts
#subject
def subject_data(tbl) :
    query = "SELECT subject, COUNT(*) FROM `{}` GROUP BY subject ;".format(tbl)
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
def progress_data(tbl) :
    query = "SELECT progress, COUNT(*) FROM `{}` WHERE progress != 'Done' GROUP BY progress ;".format(tbl)
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













