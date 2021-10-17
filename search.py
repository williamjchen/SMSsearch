import openai
import google
from constants import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


def search(search_term: str):
    result = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=search_term,
        documents=[],
        examples_context="In 2017, U.S. life expectancy was 78.6 years.",
        examples=[["What is human life expectancy in the United States?", "78 years."]],
        max_rerank=10,
        max_tokens=5,
        stop=["\n", "<|endoftext|>"]
    )
    print(result.answers)
