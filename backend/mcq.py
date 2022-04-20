from rake_nltk import Rake
import nltk
import yake
import bert
# from keybert import KeyBERT

# FOR GOOGLE QUERYING
from googlesearch import search
from bs4 import BeautifulSoup
import html
import requests
import re
import time

nltk.download('stopwords')
nltk.download('punkt')


# RAKE NLTK
# def rake_extractor(text):
#     rake_nltk_var = Rake()
#     rake_nltk_var.extract_keywords_from_text(text)
#     keyword_extracted = rake_nltk_var.get_ranked_phrases()
#     print(keyword_extracted)

def yake_extractor(text):
    # text.toLowerCase()
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                                dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    # keywords.sort()
    return keywords
    # print(keywords[0][0])
    # for kw in keywords:
    #     print(kw)


def scrape_url(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    page_source = soup.findAll('p')
    text = page_source[1].text
    question = re.sub('adver.+|\n\s+[a-z].+|\n\t\n', '', text)
    question = re.sub('(\.)\n(\d)', '\g<1>\n\n\g<2>', question)
    if("View AnswerAnswer" in question):
        question = question.replace("View AnswerAnswer","Answer")
    pattern = r"([ \t]*\d+\.[^\n]+\n(?:[ \t]*[a-zA-Z]\)[^\n]+\n)+[\s]*|(Answer:[^\n]*[\s]*Explanation:[^\n]*[\s]*))"
    return re.findall(pattern, question)
    # return question


def search_google(keywords):
    question = []
    # print(keywords)
    for i in range(5):
        query = "MCQS on " + keywords[i][0]
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            # print(j)
            if("sanfoundry" in j):
                text = scrape_url(j)
                if(len(text) > 0):
                    question.append(text)
    return question


def gen_mcq(summary):
    start_time = time.time()
    keywords = yake_extractor(' '.join(summary))
    question = search_google(keywords)
    print("Total time take for MCQ extraction is : %s seconds" %
          (time.time() - start_time))
    return question


# to search
