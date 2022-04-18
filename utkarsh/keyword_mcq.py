from rake_nltk import Rake
import nltk
import yake
import bert
# from keybert import KeyBERT

## FOR GOOGLE QUERYING
from googlesearch import search
from bs4 import BeautifulSoup
import html
import requests
import re

nltk.download('stopwords')
nltk.download('punkt')

text=open("final_recognized.txt").read()


#### RAKE NLTK 
# def rake_extractor(text):
#     rake_nltk_var = Rake()
#     rake_nltk_var.extract_keywords_from_text(text)
#     keyword_extracted = rake_nltk_var.get_ranked_phrases()
#     print(keyword_extracted)

def yake_extractor(text):
    #text.toLowerCase()
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    with open('keywords.txt','a',errors="ignore") as file:
        for kw in keywords:
            file.write(str(kw)+'\n')

    # keywords.sort()
    return keywords
    # print(keywords[0][0])
    # for kw in keywords:
    #     print(kw)

def scrape_url(url):
    data=requests.get(url)
    soup=BeautifulSoup(data.text,'html.parser')
    page_source=soup.findAll('p')
    text=page_source[1].text
    question = re.sub('adver.+|\n\s+[a-z].+|\n\t\n', '', text)
    question = re.sub('(\.)\n(\d)','\g<1>\n\n\g<2>', question)
    with open('Mcqs.txt','a',errors="ignore") as file:
        file.write("\n############## "+url+"\n")
        file.write(question)

def search_google(keywords):
    for kw in keywords:
        query = "MCQS on " + kw[0]   
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            print(j)
            if("sanfoundry" in j):
                scrape_url(j)

keywords = yake_extractor(text)
search_google(keywords)



# to search
