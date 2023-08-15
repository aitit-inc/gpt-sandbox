from dotenv import load_dotenv
import os
import openai

load_dotenv()


class Config:
    def __init__(self):
        self.ai_name = "TutorGPT"
        self.ai_role = "tutor of creating a book of questions"
        
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = str(os.getenv("MODEL"))
        self.temperature = float(os.getenv("TEMPERATURE"))
        self.max_tokens = int(os.getenv("MAX_TOKENS"))
        
        self.chapter_prefix = os.getenv("CHAPTER_PREFIX")
        self.keyword_prefix = os.getenv("KEYWORD_PREFIX")
        self.question_prefix = os.getenv("QUESTION_PREFIX")

        openai.api_key = self.openai_api_key

    def change_model(self, model: str):
        self.model = model

    def change_temperature(self, temperature: float):
        self.temperature = temperature