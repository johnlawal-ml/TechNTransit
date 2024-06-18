import streamlit as st
import pandas as pd
import os
import time

# Define the questions and choices
questions = [
    {
        "question": "Which of the following is the correct formula to add cells A1 and B1 in Excel?",
        "options": ["=A1+B1", "=SUM(A1`:`B1)", "=ADD(A1, B1)", "=A1-B1"],
        "answer": "=A1+B1"
    },
    {
        "question": "What function would you use to calculate the average of a range of cells in Excel?",
        "options": ["=MEAN()", "=AVG()", "=AVERAGE()", "=SUM()/COUNT()"],
        "answer": "=AVERAGE()"
    },
    {
        "question": "Which of the following is not a logical operator in Excel?",
        "options": ["AND", "OR", "NOT", "IF"],
        "answer": "IF"
    },
    {
        "question": "What will be the result of the formula =AND(TRUE, FALSE)?",
        "options": ["TRUE", "FALSE", "ERROR", "#VALUE!"],
        "answer": "FALSE"
    },
    {
        "question": "Which function calculates the total sum of a range in Excel?",
        "options": ["=SUM()", "=TOTAL()", "=ADD()", "=COUNT()"],
        "answer": "=SUM()"
    },
    {
        "question": "To find the smallest number in a range of cells, which function should you use?",
        "options": ["=MINIMUM()", "=LOW()", "=MIN()", "=LEAST()"],
        "answer": "=MIN()"
    },
    {
        "question": "Which of the following can you do with Conditional Formatting in Excel?",
        "options": ["Change cell values", "Format cells based on criteria", "Create Pivot Tables", "Apply data validation"],
        "answer": "Format cells based on criteria"
    },
    {
        "question": "How would you apply a color scale to a range of cells based on their values in Excel?",
        "options": ["Use the Color function", "Use Data Validation", "Use Conditional Formatting", "Use the Find and Replace tool"],
        "answer": "Use Conditional Formatting"
    },
    {
        "question": "Which function is used to search for a value in the first column of a table and return a value in the same row from a specified column?",
        "options": ["VLOOKUP", "HLOOKUP", "LOOKUP", "SEARCH"],
        "answer": "VLOOKUP"
    },
    {
        "question": "What does the FALSE parameter in the VLOOKUP function signify?",
        "options": ["Approximate match", "Exact match", "Case-insensitive match", "Case-sensitive match"],
        "answer": "Exact match"
    },
    {
        "question": "What can you use Data Validation for in Excel?",
        "options": ["To restrict the type of data that can be entered in a cell", "To perform complex calculations", "To format cells based on criteria", "To create charts and graphs"],
        "answer": "To restrict the type of data that can be entered in a cell"
    },
    {
        "question": "Which Data Validation criteria would you use to ensure a cell only accepts dates?",
        "options": ["Text Length", "List", "Date", "Custom"],
        "answer": "Date"
    },
    {
        "question": "Which of the following is true about Pivot Tables in Excel?",
        "options": ["They are used to summarize and analyze data", "They automatically update when the source data changes", "They are a type of chart", "They require complex formulas to create"],
        "answer": "They are used to summarize and analyze data"
    },
    {
        "question": "How can you refresh a Pivot Table to reflect changes in the source data?",
        "options": ["Right-click the Pivot Table and select Refresh", "Double-click any cell in the Pivot Table", "Click Insert and then Refresh", "Delete the Pivot Table and create a new one"],
        "answer": "Right-click the Pivot Table and select Refresh"
    },
    {
        "question": "Which function counts the number of cells that contain numbers in a range?",
        "options": ["=COUNT()", "=COUNTA()", "COUNTIF()", "COUNTBLANK()"],
        "answer": "=COUNT()"
    },
    {
        "question": "Which logical function returns TRUE if any of its arguments are TRUE?",
        "options": ["OR", "AND", "NOT", "IF"],
        "answer": "OR"
    },
    {
        "question": "To find the largest number in a range of cells, which function should you use?",
        "options": ["=MAXIMUM()", "=HIGH()", "=MAX()", "=MOST()"],
        "answer": "=MAX()"
    },
    {
        "question": "What is the shortcut to create a new Pivot Table in Excel?",
        "options": ["Ctrl + N", "Alt + P", "Alt + N + V", "Ctrl + T"],
        "answer": "Alt + N + V"
    },
    {
        "question": "How can you highlight cells in Excel that are greater than a specific value?",
        "options": ["Use Data Validation", "Use Find and Replace", "Use Conditional Formatting", "Use Text to Columns"],
        "answer": "Use Conditional Formatting"
    },
    {
        "question": "What function would you use to look up a value in a row and return a value from the same column?",
        "options": ["VLOOKUP", "HLOOKUP", "LOOKUP", "SEARCH"],
        "answer": "HLOOKUP"
    }

]

# Path to the results file
results_file = "quiz_results.csv"
total_time = 20 * 60  # 20 minutes in seconds

# Function to save student details and scores
def save_results(student_name, student_email, score):
    if not os.path.exists(results_file):
        # Create the file with headers if it doesn't exist
        with open(results_file, "w") as f:
            f.write("Name,Email,Score\n")

    # Append the student's details and score to the file
    with open(results_file, "a") as f:
        f.write(f"{student_name},{student_email},{score}\n")

# Function to load existing student data
def load_existing_data():
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    else:
        return pd.DataFrame(columns=["Name", "Email", "Score"])

# Display the logo at the top
st.image("logo.png", width=100)  # Adjust width as needed

# Title of the quiz
st.title("Class Quiz")

# Sidebar for student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_email = st.sidebar.text_input("Email")

# Remove admin access for jolawal8@gmail.com
admin_emails = []  # Empty list means no admin access

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Load existing student data to check for duplicates
existing_data = load_existing_data()

if student_email in existing_data["Email"].values and student_email not in admin_emails:
    st.sidebar.warning("You have already submitted your answers. Thank you!")
elif student_name and student_email:
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = total_time - elapsed_time

    if remaining_time <= 0:
        st.session_state.submitted = True
        remaining_time = 0
    else:
        # Display the countdown timer
        st.sidebar.markdown(f"Time remaining: **{int(remaining_time // 60)}:{int(remaining_time % 60):02d}**")

        # Display current question and options
        current_question = st.session_state.current_question
        question = questions[current_question]
        st.markdown(f"**Question {current_question + 1}:** {question['question']}")
        st.session_state.student_responses[current_question] = st.radio(
            f"Select your answer for Question {current_question + 1}:", question["options"], key=current_question
        )

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        if current_question > 0:
            if col1.button("Previous"):
                st.session_state.current_question -= 1

        if current_question < len(questions) - 1:
            if col3.button("Next"):
                st.session_state.current_question += 1
        else:
            if col3.button("Submit"):
                st.session_state.submitted = True

                # Submit quiz
                if not student_name or not student_email:
                    st.error("Please fill in both your name and email.")
                else:
                    correct_answers = 0
                    total_questions = len(questions)

                    for i, q in enumerate(questions):
                        if st.session_state.student_responses.get(i) == q["answer"]:
                            correct_answers += 1

                    # Save student details and score
                    save_results(student_name, student_email, correct_answers)

                    # Display results
                    st.write(f"You answered {correct_answers} out of {total_questions} questions correctly.")

                    # Feedback message
                    if correct_answers == total_questions:
                        st.success("Excellent! You got all questions right!")
                    elif correct_answers >= total_questions / 2:
                        st.info("Good job! You got more than half of the questions right.")
                    else:
                        st.warning("You need more practice. Better luck next time!")

                    st.sidebar.success("Details submitted successfully!")

                    # End the quiz
                    st.error("Time's up! Your quiz has been automatically submitted.")

# Admin section to download results
st.sidebar.title("Admin Section")
if st.sidebar.checkbox('Show download link for results'):
    if os.path.exists(results_file):
        with open(results_file, 'rb') as f:
            st.sidebar.download_button(
                label='Download Results',
                data=f,
                file_name=results_file,
                mime='text/csv'
            )
    else:
        st.sidebar.write("No results available yet.")