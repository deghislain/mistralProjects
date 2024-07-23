from PyPDF2 import PdfReader

import mistral_client as mc
from rich import print_json
import streamlit as st
import json

is_document_loaded = False


def extract_text_from_pdf():
    global is_document_loaded
    label = "Upload a PDF document here"
    file = st.file_uploader(label, type=['pdf'], accept_multiple_files=False, key=None, help=None, on_change=None,
                            args=None, kwargs=None, disabled=False, label_visibility="visible")
    text = ""
    if file is not None:
        is_document_loaded = True
        reader = PdfReader(file)
        for page in reader.pages:
            text = text + page.extract_text()
    return text


text_document = extract_text_from_pdf()
print(text_document)
example_response = """
{{
            "questions":{
                            { 
                                "question": "What are large language models?",
                                "answers": {
                                        "A": "Large language models are advanced artificial intelligence systems that take some input and generate humanlike text as a response."
                                        "B": "Large language models are AI protocols."
                                        "C": "Large language models are a type of neural networks."
                                },
                               "solution": "A"
                            },
                            { 
                                "question": "How does Large language models work?",
                                "answers": {
                                        "A": "They work by generating casual text"
                                        "B":  "They work by first analyzing vast amounts of data and creating an internal structure that models"
                                                the natural language data sets that they’re trained on."
                                        "C":  "Large language models just use statistic an internet to generate text"
                                },
                               "solution": "B"
                            }
        
        }}  
"""

prompt = f""" 
        Context information is below.
        ---------------------
        {text_document}
        ---------------------
        You are an AI teacher. Given the context information and not prior knowledge, 
        your task is to generate a list of 5 questions with answers.
        The questions shall test the level of knowledge of your student regarding the content of this {text_document}.
        You will return a response in json format. Each question must have 3 answers in the multiple choice question style.
        Only one response shall be correct. The correct answer shall be labeled as solution.
        
        Here are some examples of questions with their respective answers and solutions in json schema:
       
        {example_response}
         
"""


def get_the_questionnaire():
    if 'questions' not in st.session_state:
        resp = mc.mistral(prompt, is_json=True)
        json_resp = json.loads(resp)
        questions = json_resp["questions"]
        st.session_state['questions'] = questions
        st.session_state['current_question_number'] = 0
        print_json(resp)


def get_user_answer(quest):
    st.write(':blue[' + quest["question"] + ']')
    answers = quest["answers"]
    resp_a = st.checkbox(answers["A"])
    resp_b = st.checkbox(answers["B"])
    resp_c = st.checkbox(answers["C"])

    if resp_a:
        return "A"
    elif resp_b:
        return "B"
    elif resp_c:
        return "C"
    else:
        return ""



def next_question():
    if 'current_question_number' in st.session_state:
        curr_quest_num = st.session_state['current_question_number']
        return st.session_state['questions'][curr_quest_num]


def check_answer(q, user_resp):
    msg = ""
    is_correct = False
    if user_resp is not "":
        if q['solution'] is user_resp:
            msg = "Correct Answer"
            cqt = st.session_state['current_question_number']
            st.session_state['current_question_number'] = cqt + 1
            is_correct = True
        else:
            msg = "Wrong Answer"

        st.write(':red[ '+ msg+']')
    return is_correct


def show_question():
    st.experimental_rerun()
    q = next_question()
    u_resp = get_user_answer(q)
    check_answer(q, u_resp)
    st.button("Check Answer")


get_the_questionnaire()
q = next_question()
user_resp = get_user_answer(q)
if st.button("Check Answer"):
    if check_answer(q, user_resp):
        show_question()
