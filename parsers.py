# -*- coding: utf-8 -*-
# PROCEDURE: Read from list of URLS -> grab first two paragraphs
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import requests
import re
import nltk
from nltk.corpus import stopwords
import collections

def small_clean(xstr):
    if xstr is None:
        xstr = ""
        return xstr
    else:    
        xstr = "".join([x if ord(x) < 128 else ' ' for x in xstr])
        xstr=re.sub(r"\n"," ",xstr)
        xstr=re.sub(r"\r"," ",xstr)
        xstr=re.sub(r"\t"," ",xstr)
        xstr=re.sub(r"`"," ",xstr)
        xstr=re.sub(r"--"," ",xstr)
        xstr = re.sub(r'[^\w]', ' ', xstr)
        xstr = ' '.join(xstr.split())
        xstr = xstr.encode('utf-8').strip()
        xstr=str(xstr)
        return xstr      

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r'<[^>]*?>', '',value)

def keyword_parse(textblob):
    noun_list = []
    verb_list = []
    textblob = small_clean(textblob)
    text = nltk.word_tokenize(textblob)
    text = [w for w in text if not w in stopwords.words('english')]
    output = nltk.pos_tag(text)
    for element in output:
        noun_element = ""
        verb_element = ""
        if "NN" in str(element[1]):
            noun_element = element[0].lower()
            noun_list.append(noun_element)
        if "VB" in str(element[1]):
            verb_element = element[0].lower()
            verb_list.append(verb_element)
    return noun_list, verb_list    

def pos_counter(pos_list):
    pos_count = collections.Counter(pos_list)
    pos_counts = pos_count.most_common()
    return pos_counts


def think_bank_parser(think_tank_name):
    publications = []
    superblob = ""

    base_url = "http://www.think-bank.org/searchform.php?aut=&tit=&top=education"

    page = requests.get(base_url,timeout=120)
    souper = BeautifulSoup(page.content)

    listblob = souper.findAll('td')[1].findAll('i')

    #print listblob

    print len(listblob)

    for numb in range(0,len(listblob)):
        result = {}
        institution = souper.findAll('td')[1].findAll('i')[numb].getText()
        institution = small_clean(institution)
        #print institution
        if think_tank_name in institution:
            title = souper.findAll('td')[1].findAll('a')[numb].getText()
            print title
            url = souper.findAll('td')[1].findAll('a')[numb].attrs.get('href')
            print url    
            date = souper.findAll('td')[1].findAll('b')[numb+1].getText()
            print date

            result['title'] = title
            result['url'] = url
            result['date'] = date
            publications.append(result)

            sub_url = url
            page = requests.get(sub_url,timeout=120)
            subsouper = BeautifulSoup(page.content)
            for script in subsouper('script'):
                script.extract()
                subsouperstr = strip_tags(str(subsouper))
                superblob = superblob + subsouperstr
    return publications, superblob

def parse_all(institution_list):
    all_text = ""
    for institution in institution_list:
        institution.publications, add_to_text = think_bank_parser(institution.name)
        all_text = all_text + add_to_text

    nouns, verbs = keyword_parse(all_text)

    noun_counts = pos_counter(nouns)
    print noun_counts
    verb_counts = pos_counter(verbs)
    print verb_counts

    return noun_counts,verb_counts

def parse_by_politics(ideology, institution_list):
    all_text = ""
    for institution in institution_list:
        if str(institution.political_alignment) == str(ideology):
            institution.publications, add_to_text = think_bank_parser(institution.name)
            all_text = all_text + add_to_text

    nouns, verbs = keyword_parse(all_text)

    noun_counts = pos_counter(nouns)
    print noun_counts
    verb_counts = pos_counter(verbs)
    print verb_counts

    return noun_counts,verb_counts

def parse_by_institution(think_tank_name):
    institution.publications, all_text = think_bank_parser(think_tank_name)
    nouns, verbs = keyword_parse(all_text)

    print noun_counts
    verb_counts = pos_counter(verbs)
    print verb_counts

    return noun_counts,verb_counts    