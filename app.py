import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

prompt_one = PromptTemplate(
    template="""You are a medical assistant specifically for cricketers. If a cricketer faces any problem, 
respond like this:
1. Reason behind the problem.
2. How to recover.
3. Recommended medicines.
4. Steps to avoid this issue in the future.

Problem: {input_problem}""",
    input_variables=["input_problem"]
)

prompt_two = PromptTemplate(
    template="""Translate the following medical response into the national language of the cricket team: {cricket_team_name}

Medical Response:
{medical_response}""",
    input_variables=["cricket_team_name", "medical_response"]
)

model = ChatGroq(
    model="llama3-70b-8192",
    api_key=GROQ_KEY,
    temperature=0.7
)

parser = StrOutputParser()

chain_one = prompt_one | model | parser
chain_two = prompt_two | model | parser

def get_medical_response(problem, team):
    medical_answer = chain_one.invoke({"input_problem": problem})
    translated_answer = chain_two.invoke({
        "cricket_team_name": team,
        "medical_response": medical_answer
    })
    return {
        "input_problem": medical_answer,
        "input_language": translated_answer
    }

st.set_page_config(page_title="Cricketer Medical Chatbot")
st.title("🏏 Cricketer Medical Assistant")

input_problem = st.text_input("Describe your medical issue:")
input_team = st.text_input("Your cricket team name:")

if st.button("Get Advice"):
    if input_problem and input_team:
        with st.spinner("Thinking..."):
            result = get_medical_response(input_problem, input_team)
            st.subheader("🩺 Medical Advice:")
            st.write(result["input_problem"])
            st.subheader("🌐 Translated Advice:")
            st.write(result["input_language"])
    else:
        st.warning("Please fill in both fields.")

