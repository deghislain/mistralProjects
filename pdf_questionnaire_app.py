from PyPDF2 import PdfReader
import question_generator as qg
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


if not is_document_loaded:
    text_document = extract_text_from_pdf()

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
        The following text document is about large language model.
        ---------------------
        {text_document}
        ---------------------
        You are an AI teacher. Given the text document and not prior knowledge.
        your task is to generate a list of 5 questions with answers.
        The instructions for this task are as follow:
        All generated questions must come from the provided text document content.
        You will return a response in json format. Each question must have 3 answers in the multiple choice question style.
        Only one response shall be correct. The correct answer shall be labeled as solution.

        Here are some examples of questions with their respective answers and solutions in json schema:

        {example_response}

"""

def get_the_questionnaire():
    test_status = ""
    if 'test_status' in st.session_state:
        test_status = st.session_state['test_status']
    if 'questions' not in st.session_state or test_status == "completed":
        resp = mc.mistral(prompt, is_json=True)
        json_resp = json.loads(resp)
        questions = json_resp["questions"]
        st.session_state['questions'] = questions
        st.session_state['current_question_number'] = 0
        st.session_state['score'] = 0
        if test_status == "completed":
            st.session_state['test_status'] = "new_test"
        elif test_status == "":
            st.session_state['test_status'] = "loaded"

        print_json(resp)

if __name__ == "__main__":
    if is_document_loaded:
        get_the_questionnaire()
        qg.start_test()
