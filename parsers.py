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
    text = nltk.word_tokenize(textblob)
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
    pos_counter = collections.Counter(pos_list)
    pos_counts = pos_counter.most_common()
    return pos_counts

'''
def heritage_foundation_scrape(publications.base_url):
    display = Display(visible=0, size=(800,600))
    display.start()
    driver = webdriver.Firefox()
    driver.get(base_url)

    report_xpath = '//*[@id="LoadMoreReports"]'
    clicker = driver.find_elements_by_xpath(report_xpath)[0]
    clicker.send_keys(Keys.END)
    clicker.click()
    time.sleep(5)
    page = driver.page_source
    souper = BeautifulSoup(page)

    strsouper = str(souper)
    all_reports = souper.findAll('ul',{"id":"LoadResearchRecords"})[0].findAll('li')

    string_blob = ""

    for numb in range(0,len(all_reports)):
        #print all_reports[numb].getText()
        authors = []
        try:
            author_list = all_reports[numb].findAll('a',{"class":"author-link"})
            #print author_list
            for author in author_list:
                #print author
                authors.append(author.getText())
            #raw_input()
        except:
            pass
        print authors
        title = all_reports[numb].findAll('a',{"class":"item-title"})[0].getText()
        print title
        url = all_reports[numb].findAll('a')[0].attrs.get('href')
        print url
        amended_url = "http://www.heritage.org/" + url

        month = url.split('/')[-2]
        year = url.split('/')[-3]

        print str(month) + " | " + str(year)
        #print amended_url
        page = requests.get(amended_url,timeout=120)
        subsouper = BeautifulSoup(page.content)
        for script in subsouper('script'):
            script.extract()
        subsouperstr = strip_tags(str(subsouper))
        #print subsouperstr
        string_blob = string_blob + " " + subsouperstr

    string_blob = small_clean(string_blob)
    #print string_blob
    n_list,v_list = keyword_parse(string_blob)
    noun_counts = pos_counter(n_list)
    verb_counts = pos_counter(v_list)


    print noun_counts[:30]
    open("noun_sample.txt",'w').write(str(noun_counts))
    print verb_counts[:30]    
    open("verb_sample.txt",'w').write(str(verb_counts))

    driver.close()
    driver.quit() 
    display.stop()
'''

'''
'''
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
        print institution
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
            page = requests.get(suburl,timeout=120)
            subsouper = BeautifulSoup(page.content)
            for script in subsouper('script'):
                script.extract()
                subsouperstr = strip_tags(str(subsouper))
                superblob = superblob + subsouperstr
    return publications, superblob