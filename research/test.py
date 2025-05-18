# medical_chatbot.py

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableParallel
import os

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

prompt_one = PromptTemplate(
    template="""You are a medical assistant specifically for cricketers. If a cricketer faces any problem, 
you must respond in this structure:
1. Reason behind the problem.
2. How to recover.
3. Recommended medicines.
4. Steps to avoid this issue in the future.
Problem: {input_problem}""",
    input_variables=['input_problem']
)

prompt_two = PromptTemplate(
    template="""Respond in the national language of the cricket team: {cricket_team_name}""",
    input_variables=['cricket_team_name']
)

model = ChatGroq(
    model="llama3-70b-8192",
    api_key=GROQ_KEY,
    temperature=0.7
)

parser = StrOutputParser()

chain_one = prompt_one | model | parser
chain_two = prompt_two | model | parser

parallel_chain = RunnableParallel(
    input_problem=chain_one,
    input_language=chain_two
)

def get_medical_response(problem, team_name):
    result = parallel_chain.invoke({
        "input_problem": problem,
        "cricket_team_name": team_name
    })
    return result
