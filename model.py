import os
from dotenv import load_dotenv
from transform import extract_text_from_fitz
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate

load_dotenv()

class TeacherModel:
    def __init__(self, document):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.model = ChatOpenAI(temperature=0.2, model='gpt-4o-mini')
        self.output_parser = StrOutputParser()
        self.document = document
        self.sys_p = None
        self.user_p = None

    def sys_prompt(self, sys_p):
        self.sys_p = sys_p
        system_prompt = SystemMessagePromptTemplate.from_template(sys_p)
        return system_prompt
    
    def user_prompt(self, user_p):
        self.user_p = user_p
        if not self.document.strip():
            raise ValueError("The document is empty.")
        
        if len(self.document) > 10000:
            self.document = self.document[:10000]

        human_prompt = HumanMessagePromptTemplate.from_template(user_p + "{document}")
        return human_prompt
    
    def main_prompt(self):
        if self.sys_p is None or self.user_p is None:
            raise ValueError("System and user prompts must be set before calling main_prompt")
        return ChatPromptTemplate.from_messages([
            self.sys_prompt(self.sys_p), 
            self.user_prompt(self.user_p)
        ])
    
    def stream_response(self):
        prompt = self.main_prompt()
        chain = prompt | self.model | self.output_parser

        print("🧠 Streaming summary...\n")
        for chunk in chain.stream({"document": self.document}):
            print(chunk, end="", flush=True)

pdf_file = "DSP - Lecture Notes (Chapter 1).pdf"
document = extract_text_from_fitz(pdf_file)
model = TeacherModel(document=document)
    
model.sys_prompt(sys_p="You are an AI Assistant designed to tutor data science and statistics. Summarize the provided notes in a well-structured format with an introduction, body, and conclusion.")
model.user_prompt(user_p="Please provide a comprehensive summary of these notes in three paragraphs:\n\n")
result = model.response()
print(result)