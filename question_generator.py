import PyPDF2
from PyPDF2 import PdfReader

import mistral_client as mc
from rich import print_json
import streamlit as st
import json


def extract_text_from_pdf():
    label = "Upload a PDF document here"
    file = st.file_uploader(label, type=['pdf'], accept_multiple_files=False, key=None, help=None, on_change=None,
                            args=None, kwargs=None, disabled=False, label_visibility="visible")
    text = ""
    if file is not None:
        reader = PdfReader(file)
        for page in reader.pages:
            text = text + page.extract_text()
    return text


text_document = extract_text_from_pdf()
print(text_document)
print("---------------------------------------------------------------------------")
example_response ="""
{{
            "questions":{
                            { 
                                "question": "What are large language models?",
                                "answers": {
                                        "A": "Large language models are advanced artificial intelligence systems that take some input and generate humanlike text as a response."
                                        "B": "Large language models are AI protocols."
                                        "C": "Large language models are a type of neural networks."
                                },
                               "solution": "answer A"
                            },
                            { 
                                "question": "How does Large language models work?",
                                "answers": {
                                        "A": "They work by generating casual text"
                                        "B":  "They work by first analyzing vast amounts of data and creating an internal structure that models"
                                                the natural language data sets that they’re trained on."
                                        "C":  "Large language models just use statistic an internet to generate text"
                                },
                               "solution": "answer B"
                            }
        
        }}  
"""

prompt =f""" 
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


def print_questions_answers(response):
    json_resp = json.loads(response)
    questions = json_resp["questions"]
    for q in questions:
        st.header(':blue[' + q["question"] + ']')
        answers = q["answers"]
        st.write(answers["A"])
        st.write(answers["B"])
        st.write(answers["C"])


if text_document != "":
    response = mc.mistral(prompt, is_json=True)
    print_json(response)

    print_questions_answers(response)
