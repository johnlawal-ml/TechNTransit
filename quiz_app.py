import streamlit as st
import pandas as pd
import time

st.title('Class Quiz with Timer')

student_name = st.text_input('Enter Your Name:')
student_email = st.text_input('Enter Your Email:')

quiz_time = st.slider('Set Quiz Time (in minutes):', 1, 60, 5)

start_quiz = st.button('Start Quiz')

if start_quiz:
    st.write(f'Quiz Started for {student_name}!')
    end_time = time.time() + quiz_time * 60

    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        st.write(f'Time Remaining: {remaining_time // 60} minutes {remaining_time % 60} seconds')
        time.sleep(1)

    st.write('Quiz Ended!')
    st.write('Downloading Results...')

    # Mock quiz results data
    quiz_results = {
        'Question 1': ['A', 'B', 'C'],
        'Question 2': ['B', 'A', 'C'],
        'Question 3': ['C', 'B', 'A']
    }

    df = pd.DataFrame(quiz_results)
    st.write(df)

    st.markdown(f"### [Download Results as Excel](data:file/csv;base64,{df.to_csv().encode().decode('utf-8').encode('latin-1').hex()})")