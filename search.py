import openai
from googlesearch import search
import bs4
import requests
from constants import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


def search_gpt(search_term: str):
    articles = []
    for link in search(search_term, tld="co.in", num=5, stop=5, pause=2):
        print(link)
        re_result = requests.get(link)
        soup = bs4.BeautifulSoup(re_result.text, "html.parser")
        for paragraph in soup.find_all('p'):
            articles += [paragraph.get_text()]
    print(articles)

    result = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=search_term,
        documents=articles[:200],
        examples_context="Cattle, taurine cattle, or European cattle (Bos taurus or Bos primigenius taurus) are large domesticated cloven-hooved herbivores. They are a prominent modern member of the subfamily Bovinae, are the most widespread species of the genus Bos. Depending on sex, they are referred to as cows (female) or bulls (male).",
        examples=[["What is a cow?", "Depending on sex, cattle are referred to as cows (female) or bulls (male)."]],
        max_rerank=10,
        max_tokens=15,
        stop=["\n", "<|endoftext|>"]
    )
    print(result.answers)
    return result.answers[0]
