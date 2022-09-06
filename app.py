import streamlit as st
import pandas as pd  #EDA package
import db ##my database helper file
from matplotlib import pyplot as plt  #for pie charts



#tbl --> name of the table to be used for this user
def main(tbl_name) :
    #table name session state
    if "tbl" not in st.session_state :
        st.session_state['tbl'] = tbl_name
    
    tbl = st.session_state['tbl']
    #cant directly use tbl_name 
    #as its value gets initialised to null everytime we interact with a widget
    
    #beautification
    st.title("Assignment tracker")

    #displaying gif
    st.image(
            "https://media.giphy.com/media/WRRL1EKo9rNe12S4zh/giphy.gif", 
            use_column_width=True, 
        )


    #side bar
    #dropbox
    #options to be given in the drop box
    menu = ["Home" , "Add assignment", "Edit an assignment" ,"Stats"]
    #create the dropbox
    choice = st.sidebar.selectbox("Menu", menu)
      #dropbox heading is "menu"
      #option selected is stored in the var "choice"


    #####display###############################
    if choice=="Home" :
        #display assignments
        #create the subject list
        subject_list = db.get_sub_list(tbl)

        #variables get re-initialised whenever we interact with a widget
        #so there wont be multiple "All" in the list
        #select what assignment to display

        display_what = st.selectbox( "Select subject", subject_list)
        #"All" or subject name

        ##########display all###########################
        if display_what == "All" :
            #then display all assignments
            tasks = db.display_all(tbl)

            #using pandas dataframes to 
            #display the tasks in a tabular format
            df = pd.DataFrame(tasks, columns=["Assignment", "Subject", "Due date", "Progress"])
            #col headings given

            #display the dataframe
            st.dataframe(df)

        ############display only 1 subject############
        else :
            tasks = db.display_subject_tasks(tbl, display_what) 
            #display the tasks in a tabular format
            df = pd.DataFrame(tasks, columns=["Assignment", "Subject", "Due date", "Progress"])
            #col headings given
            #display the dataframe
            st.dataframe(df)

        #delete all button
        if st.button("Delete all") :
            db.clear(tbl)


    ######adding assignment##########################
    if choice=="Add assignment" :
        with st.form("my_form", clear_on_submit=True) :
            st.subheader("Add assignment")

            #textbox
            assgn = st.text_area("Assignment")
            #selectbox
            progress = st.selectbox( "Progress",["Not started", "Started" , "Done"])
            #due date
            due = st.date_input("Due date")
            #subject
            subject = st.text_input("Subject")

            #"done" button
            if st.form_submit_button("Add") :
                #add data to table
                    #function from db.py file
                db.add_assgn(tbl ,assgn , progress , due, subject)
                #success message
                st.success("Assignment added successfully!")


    ##### edit an assignment #######################################
    if choice=="Edit an assignment" :
        st.subheader("Edit assignment")

        #select the assgn to edit ############################
        #create the assgn list
        subject_list = db.get_assignment_list(tbl)
        
        #select what assignment to edit
        assgn_to_edit = st.selectbox( "Select assignment to edit", subject_list)

        #edit the assignment######################################
        #form
        with st.form("my_form", clear_on_submit=True) :
            new_progress = st.selectbox( "Update progress",["Not started", "Started" , "Done"])
            new_due = st.date_input("Update due date")

            #buttons#########################################################
            #"save" button
            if st.form_submit_button('Save changes') :
                #add update the data in the table
                db.edit_assgn(tbl, assgn_to_edit, new_progress , new_due)
                #success message
                st.success("Assignment updated successfully!")

        #delete assignment button ##################################
        if st.button("Delete assignment") :
            db.delete_assignment(tbl, assgn_to_edit)
            #dont save the changes made
            st.warning("Assignment deleted.")

    #stats
    elif choice=="Stats" :
        #display subjctwise piechart
        st.subheader("Subjectwise share of assignments")
        tup = db.subject_data(tbl)
        #tup[0] --> subject list
        #tup[1] --> count list

        #plotting the pie chart
        fig = plt.figure()
        plt.pie(tup[1], labels = tup[0], autopct='%1.1f%%')
        
        # show plot
        st.write(fig)

        ###################################################################################
        #display subjctwise piechart
        st.subheader("Progress made on pending assignments")
        tup = db.progress_data(tbl)
        #tup[0] --> progress list
        #tup[1] --> count list

        #plotting the pie chart
        fig = plt.figure()
        plt.pie(tup[1], labels = tup[0], autopct='%1.1f%%')
        
        # show plot
        st.write(fig)



      

    
    
