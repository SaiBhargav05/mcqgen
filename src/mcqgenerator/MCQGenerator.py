import os
import json
import traceback 
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

## import necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


load_dotenv()

key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(openai_api_key = key, model_name = "gpt-4.1-mini", temperature=0.7)


template="""
Text: {text}

You are an expert MCQ maker. Given the above text, your job is to
create a quiz of {number} multiple-choice questions for {subject} students in a {tone} tone.

Make sure:
- The questions are not repeated.
- All questions strictly conform to the text.
- The number of MCQs is exactly {number}.
- Format your output like the RESPONSE_JSON example below.

### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template= template

)

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

template2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students,\
you need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity.
If the quiz is not at par with the cognitive and analytical abilities of the student,\
update the quiz questions which need to be changed and change the tone so that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template = template2)

review_chain = LLMChain(llm = llm, prompt = quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)







