import streamlit as st
import db ##my database helper file
import app #app.py file


def authentication():
    #dict of users #email : password
    user_dict = db.getUsers()
            
    #####################################################################   working well
    #if email is already registered and pw is correct 
    #if dict.get(email) == password
    if user_dict.get(st.session_state["email"]) == st.session_state["password"]:
        st.success("Welcome back!\n")

        #use the table for this user
        tbl_name = str( st.session_state["email"] )

        if "tbl" not in st.session_state :
            st.session_state['tbl'] = tbl_name

        #set auth_done to True
        st.session_state["auth_done"] = True


    #if email record doesnt exist in the dict #new user
    elif user_dict.get(st.session_state["email"]) == None:
        #add user info to the table
        e = str( st.session_state["email"] )
        p = str( st.session_state["password"] )
        db.addUser( e,p)

        #table name for this user
        tbl_name = st.session_state["email"] 
        #use this table in this session
        #create the table    
        db.create_table(tbl_name)

        #set auth_done to True
        st.session_state["auth_done"] = True

        #success message
        st.success("New user registred. Welcome!")


    #if email already registered, but password is incorrect
    else :
        st.error("Password is incorrect. Try again\n")


#######################################################################################
#########################################################################################

#driver code starts from here
#boolean
if "auth_done" not in st.session_state :
    st.session_state['auth_done'] = False

#defining the session state variables
if "email" not in st.session_state :
    st.session_state['email'] = ""
if "password" not in st.session_state :
    st.session_state['password'] = ""


#if authentication hasnt been done yet
if st.session_state['auth_done'] == False :
    #email, password input
    with st.form("Sign in", clear_on_submit=True) :
        st.text_input("Email", key="email")
        #when email id is enterred, password_entered() funct is called
        st.text_input("Password", type="password", key="password")  

        if st.form_submit_button("Enter") :
            #call the authentication function
            authentication()


#after authentication, proceed with the rest of the app
if st.session_state['auth_done'] == True :
    #table name for this user
    tbl = st.session_state["email"]

    #calling the main function from app.py file
    app.main(tbl) 
    #define session state for table name again in the main()
    #as session state cant be passed through function ???



