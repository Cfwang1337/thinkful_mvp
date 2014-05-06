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

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r'<[^>]*?>', '',value)

base_url = "http://www.heritage.org/issues/education"

'''
def heritage_foundation_scrape(publications,base_url):
open(file_name,'w').write(str(souper.prettify))
file_name = "sample.txt"
'''    


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
#print souper.prettify()
strsouper = str(souper)
all_reports = souper.findAll('ul',{"id":"LoadResearchRecords"})[0].findAll('li')
#print len(all_reports)
noun_list = []
verb_list = []
for numb in range(0,len(all_reports)):
    #print all_reports[numb].getText()
    url = all_reports[numb].findAll('a')[0].attrs.get('href')
    amended_url = "http://www.heritage.org/" + url
    #print amended_url
    page = requests.get(amended_url,timeout=120)
    subsouper = BeautifulSoup(page.content)
    for script in subsouper('script'):
        script.extract()
    subsouperstr = strip_tags(str(subsouper))
    #print subsouperstr
    text = nltk.word_tokenize(subsouperstr)
    output = nltk.pos_tag(text)

    #print len(output)
    #print output[0]

    for element in output:
        noun_element = ""
        verb_element = ""
        if "NN" in str(element[1]):
            noun_element = element[0].lower()
            noun_list.append(noun_element)
        if "VB" in str(element[1]):
            verb_element = element[0].lower()
            verb_list.append(verb_element)

    #print noun_list
    #print verb_list

    '''
    text_counter = collections.Counter(text)
    text_counts = text_counter.most_common()
    file_name = "sample.txt"
    print text_counts
    raw_input()
    '''

noun_counter = collections.Counter(noun_list)
noun_counts = noun_counter.most_common()

verb_counter = collections.Counter(verb_list)
verb_counts = verb_counter.most_common()
print noun_counts
open("noun_sample.txt",'w').write(str(noun_counts))
print verb_counts    
open("verb_sample.txt",'w').write(str(verb_counts))

driver.close()
driver.quit() 
display.stop()   