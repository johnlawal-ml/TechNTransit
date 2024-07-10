import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to format the timer
def format_time(t):
    minutes, seconds = divmod(t.seconds, 60)
    return f"{minutes:02}:{seconds:02}"

# Countdown time in minutes
countdown_time = 20

# Initialize session state
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
    st.session_state.time_left = None
    st.session_state.test_started = False

# Start the test
if not st.session_state.test_started:
    st.title("Student Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    start_button = st.button("Start Test")
    
    if start_button:
        if name and email:
            st.session_state.start_time = datetime.now()
            st.session_state.time_left = timedelta(minutes=countdown_time)
            st.session_state.test_started = True
            st.session_state.name = name
            st.session_state.email = email
        else:
            st.warning("Please provide your full name and email before starting the test.")

# Test in progress
if st.session_state.test_started:
    # Calculate the time left
    st.session_state.time_left = timedelta(minutes=countdown_time) - (datetime.now() - st.session_state.start_time)

    # Display the timer
    st.title("Quiz with Countdown Timer")
    st.write("Time Left: ", format_time(st.session_state.time_left))

    # Stop the quiz if the time is up
    if st.session_state.time_left.total_seconds() > 0:
        with st.form(key='quiz_form'):
            # Example multiple-choice questions with correct answers
            questions = {
                "Question 1: What is the capital of France?": {"options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
                "Question 2: What is 2 + 2?": {"options": ["3", "4", "5", "6"], "answer": "4"},
                "Question 3: Who wrote 'Hamlet'?": {"options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"], "answer": "William Shakespeare"},
            }

            responses = {}
            for question, data in questions.items():
                responses[question] = st.radio(question, data["options"])

            # Submit button
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Calculate score
                score = 0
                for question, data in questions.items():
                    if responses[question] == data["answer"]:
                        score += 1

                # Save the results to an Excel file
                results = {
                    "Full Name": [st.session_state.name],
                    "Email": [st.session_state.email],
                    "Score": [score],
                    "Submission Time": [datetime.now()]
                }

                for question, response in responses.items():
                    results[question] = [response]
                
                df = pd.DataFrame(results)
                file_path = "student_results.xlsx"
                
                try:
                    existing_df = pd.read_excel(file_path)
                    df = pd.concat([existing_df, df], ignore_index=True)
                except FileNotFoundError:
                    pass
                
                df.to_excel(file_path, index=False)
                
                st.write("Your answers have been submitted.")
                st.write(f"Your score is: {score}/{len(questions)}")
                st.session_state.test_started = False
    else:
        st.write("Time is up! Please submit your answers.")
        st.session_state.test_started = False

# Refresh every second if the test is in progress
if st.session_state.test_started:
    st.experimental_rerun()
