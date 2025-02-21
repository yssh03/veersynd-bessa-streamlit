from openai import OpenAI
from utils import text_to_vector, get_cosine
from keyword_extractor import KeyphraseExtractionPipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
from prompts import validation_prompt, prompt


class ResumeTailor:
    def __init__(self, api_key, resume, jd):
        self.resume = resume
        self.jd = jd
        self.client = OpenAI(api_key=api_key)
        self.keywords = []

    def extract_keywords(self):

        # model = AutoModelForTokenClassification.from_pretrained(
        #     "./model/", local_files_only=True)
        # tokenizer = AutoTokenizer.from_pretrained("penguincapo/vb-jd-kwextractor")
        model = AutoModelForTokenClassification.from_pretrained(
            "penguincapo/vb-jd-kwextractor")
        tokenizer = AutoTokenizer.from_pretrained(
            "./tokenizer/", local_files_only=True)

        extractor = KeyphraseExtractionPipeline(model, tokenizer)
        return extractor(self.jd)

    def validate_jd(self):
        self.keywords = self.extract_keywords()
        text1 = str(self.keywords)
        text2 = str(self.resume)

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine = get_cosine(vector1, vector2)
        user_prompt_validation = f"""
        Keywords : {self.keywords}
        Resume Bullet Points: {self.resume}
        Cosine Similarity: {cosine}
        """

        validation_convo = [{
            "role": "system",
            "content": validation_prompt
        },
            {
            "role": "user",
            "content": user_prompt_validation
        }]

        validation_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=validation_convo,
            temperature=0.2,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        self.flag = False if validation_response.choices[0].message.content == 'False' else True
        return self.flag

    def customize_resume(self):
        user_prompt = f"""
            Keywords : {self.keywords}
            Resume Bullet Points: {self.resume}
        """
        conversation = [{
            "role": "system",
            "content": prompt
        },
            {
            "role": "user",
            "content": user_prompt
        }
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content
