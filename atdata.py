import streamlit as st
import open_camera as oc

def data_page(db, gimg, count):
    st.title("Please fill in your data")
    name = st.text_input("Enter Your Name", placeholder="please enter your name")
    roll_no = st.text_input("Enter Your Roll Number", placeholder="please enter your Roll Number", max_chars=12)
    branch_data = ["CSE", "AI&DS", "AI&ML", "IT", "Mech", "Civil"]
    year_data = ["I yr", "II yr", "III yr", "IV yr"]
    year = st.selectbox("Select Your Year", options=year_data, index=None, placeholder="Please Select Your Year")
    branch = st.selectbox("Select Your Branch", options=branch_data, index=None, placeholder="Please Select Your Branch")
    next_button = st.button("Next")
    data = [name, roll_no, branch]

    if next_button:
        if any(not data for data in [name, roll_no, branch, year]):
            st.error("Please enter all the data")
        else:
            
            oc.save_to_firestore(name=name, roll_no=roll_no, branch=branch, gimg=gimg, db=db, count=count,year=year)
            st.title("Thank you for the data")
            st.session_state.page = 'feedback'
            st.rerun()
