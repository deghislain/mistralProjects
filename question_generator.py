import streamlit as st




def get_user_answer(quest):
    st.write(':blue[' + quest["question"] + ']  5 points ')
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
    print("next_question before")
    if 'current_question_number' in st.session_state:
        print("next_question after")
        try:
            curr_quest_num = st.session_state['current_question_number']
            return st.session_state['questions'][curr_quest_num]
        except Exception as e:
            print("Error while retrieving questions from session", e)

    return None


def update_user_score():
    if 'score' in st.session_state:
        score = st.session_state['score']
        score = score + 5
        st.session_state['score'] = score


def check_answer(q, user_resp):
    is_correct = False
    if user_resp != "":
        if q['solution'] is user_resp:
            cqt = st.session_state['current_question_number']
            st.session_state['current_question_number'] = cqt + 1
            is_correct = True
            update_user_score()
    return is_correct


def show_question():
    st.experimental_rerun()
    question = next_question()
    if question is not None:
        u_resp = get_user_answer(question)
        check_answer(question, u_resp)
        st.button("Check Answer", key="checkansws")
    st.write(':green[Test completed]')


def start_new_test():
    st.session_state['current_question_number'] = 0
    st.session_state['score'] = 0
    st.experimental_rerun()
    start_test()


def start_test():
    q = next_question()
    if q is not None:
        st.session_state['test_status'] = "running"
        user_resp = get_user_answer(q)
        if st.button("Check Answer", key="checkansw"):
            if check_answer(q, user_resp):
                st.write(':green[Correct Answer]')
                show_question()
            else:
                st.write(':red[Wrong Answer]')
    else:
        if 'score' in st.session_state:
            s = st.session_state['score']
            if s > 0:
                st.header(':blue[Test completed]')
                st.title('Your score for this test is :green['.__add__(str(s)) + ']')
                st.session_state['test_status'] = "completed"
                if st.button("Start New Test", key="newtest"):
                    start_new_test()

            else:
                st.write(':red[No question available]')
