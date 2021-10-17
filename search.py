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

    examples_list = {
        "What is": ["Cattle, taurine cattle, or European cattle (Bos taurus or Bos primigenius taurus) are large domesticated cloven-hooved herbivores. They are a prominent modern member of the subfamily Bovinae, are the most widespread species of the genus Bos. Depending on sex, they are referred to as cows (female) or bulls (male).", ["What is a cow?", "Depending on sex, cattle are referred to as cows (female) or bulls (male)."]],
        "Why is": ["Sunlight reaches Earth's atmosphere and is scattered in all directions by all the gases and particles in the air. Blue light is scattered more than the other colors because it travels as shorter, smaller waves. This is why we see a blue sky most of the time.", ["Why is the sky blue?", "Blue light is scattered more than the other colors because it travels as shorter, smaller waves"]],
        "How to": ["Take tepid baths or using cold compresses to make you more comfortable. Cold baths, ice cube baths, or alcohol baths or rubs can be dangerous and should be avoided", ["How to treat a fever?", "Take tepid baths or using cold compresses to make you more comfortable."]],
        "When is": ["Under the federal Holidays Act,[15] Canada Day is observed on July 1, unless that date falls on a Sunday, in which case July 2 is the statutory holiday. Celebratory events will generally still take place on July 1, even though it is not the legal holiday.[16] If it falls on a weekend, businesses normally closed that day usually dedicate the following Monday as a day off.[17]", ["When is canada day?", "Canada day is July 1"]],
        "Who is": ["Arnold Schwarzenegger, in full Arnold Alois Schwarzenegger, (born July 30, 1947, Thal, near Graz, Austria), Austrian-born American bodybuilder, film actor, and politician who rose to fame through roles in blockbuster action movies and later served as governor of California (2003–11).", ["Who is Arnold Schwarzenegger", "Arnold Schwarzenegger is an Austrian-born American bodybuilder, film actor, and politician"]],
        "Where is": ["The Guantanamo Bay detention camp (Spanish: Centro de detención de la bahía de Guantánamo) is a United States military prison located within Guantanamo Bay Naval Base, also referred to as Guantánamo, GTMO, and \"Gitmo\" (/ˈɡɪtmoʊ/), on the coast of Guantánamo Bay in Cuba. Of the 780 people detained there since January 2002 when the military prison first opened after the September 11, 2001 attacks, 731 have been transferred elsewhere, 39 remain there, and 9 have died while in custody.[1]", ["Where is guantanamo bay?", "The Guantanamo Bay detention camp is a United States military prison located within Guantanamo Bay Naval Base"]],
    }

    example = examples_list["What is"]
    for key in examples_list.keys():
        if key in search_term.capitalize():
            example = examples_list[key]
            break
    print(example[1])

    result = openai.Answer.create(
        search_model="ada",
        model="davinci",
        question=search_term,
        documents=articles[:200],
        examples_context=example[0],
        examples=[example[1]],
        max_rerank=10,
        max_tokens=15,
        stop=["\n", "<|endoftext|>"]
    )
    print(result.answers)
    return result.answers[0]
