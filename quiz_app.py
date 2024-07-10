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
    st.title("TechNTransit Excel Class Quiz")
    st.write("Time Left: ", format_time(st.session_state.time_left))

    # Stop the quiz if the time is up
    if st.session_state.time_left.total_seconds() > 0:
        with st.form(key='quiz_form'):
            # Example multiple-choice questions with correct answers
            questions = {
                "Question 1: What is the shortcut to save a workbook in Excel?": {"options": ["Ctrl+S", "Ctrl+P", "Ctrl+O", "Ctrl+N"], "answer": "Ctrl+S"},
                "Question 2: What function do you use to find the average of a range in Excel?": {"options": ["AVERAGE", "SUM", "MIN", "MAX"], "answer": "AVERAGE"},
                "Question 3: Which function is used to lookup a value in a table?": {"options": ["LOOKUP", "VLOOKUP", "HLOOKUP", "INDEX"], "answer": "VLOOKUP"},
                "Question 4: What does the SUMIF function do?": {"options": ["Sums values based on a condition", "Counts values based on a condition", "Averages values based on a condition", "Finds the maximum value"], "answer": "Sums values based on a condition"},
                "Question 5: How do you apply conditional formatting in Excel?": {"options": ["Home > Conditional Formatting", "Insert > Conditional Formatting", "Data > Conditional Formatting", "Formulas > Conditional Formatting"], "answer": "Home > Conditional Formatting"},
                "Question 6: What function would you use to find the average of values that meet a specific condition?": {"options": ["SUMIF", "COUNTIF", "AVERAGEIF", "IF"], "answer": "AVERAGEIF"},
                "Question 7: How do you remove duplicate values in a dataset?": {"options": ["Data > Remove Duplicates", "Home > Remove Duplicates", "Insert > Remove Duplicates", "Formulas > Remove Duplicates"], "answer": "Data > Remove Duplicates"},
                "Question 8: Which tab contains the Data Validation option?": {"options": ["Data", "Home", "Insert", "Formulas"], "answer": "Data"},
                "Question 9: What does the VLOOKUP function return?": {"options": ["The entire row", "A specific cell", "The entire column", "A single value"], "answer": "A single value"},
                "Question 10: What is a PivotTable used for?": {"options": ["Sorting data", "Filtering data", "Summarizing data", "Entering data"], "answer": "Summarizing data"},
                "Question 11: Which function would you use to count the number of cells that meet a condition?": {"options": ["COUNT", "COUNTIF", "COUNTA", "COUNTBLANK"], "answer": "COUNTIF"},
                "Question 12: How do you create a drop-down list in Excel?": {"options": ["Data > Data Validation", "Home > Data Validation", "Insert > Data Validation", "Formulas > Data Validation"], "answer": "Data > Data Validation"},
                "Question 13: What is the shortcut to format cells in Excel?": {"options": ["Ctrl+1", "Ctrl+F", "Ctrl+C", "Ctrl+P"], "answer": "Ctrl+1"},
                "Question 14: What does the CONCATENATE function do?": {"options": ["Joins two or more strings together", "Finds a substring", "Converts text to uppercase", "Replaces characters in a string"], "answer": "Joins two or more strings together"},
                "Question 15: How can you quickly copy the contents of a cell to multiple cells?": {"options": ["Drag the fill handle", "Copy and paste each cell", "Use the SUM function", "Use the COUNT function"], "answer": "Drag the fill handle"},
                "Question 16: What is the purpose of freezing panes?": {"options": ["To keep row and column headings visible while scrolling", "To prevent changes to a worksheet", "To lock the worksheet", "To protect the workbook"], "answer": "To keep row and column headings visible while scrolling"},
                "Question 17: How do you apply a filter to a dataset?": {"options": ["Data > Filter", "Home > Filter", "Insert > Filter", "Formulas > Filter"], "answer": "Data > Filter"},
                "Question 18: Which of the following is not a valid chart type in Excel?": {"options": ["Line", "Bar", "Pie", "Network"], "answer": "Network"},
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
