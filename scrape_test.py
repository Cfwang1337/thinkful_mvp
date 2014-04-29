#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import time
import datetime
import requests
import re
import os
import nltk
from bs4 import BeautifulSoup
import numpy
import collections

def small_clean(xstr):
    if xstr is None:
        xstr = ""
        return xstr
    else:    
        try:
            xstr=xstr.split(':')[1]
        except:
            pass
        xstr = "".join([x if ord(x) < 128 else ' ' for x in xstr])
        xstr=re.sub(r"\n"," ",xstr)
        xstr=re.sub(r"\r"," ",xstr)
        xstr=re.sub(r"\t"," ",xstr)
        xstr=re.sub(r"`"," ",xstr)
        xstr=re.sub(r"--"," ",xstr)
        xstr = ' '.join(xstr.split())
        xstr = xstr.encode('utf-8').strip()
        xstr=str(xstr)
        return xstr      

class Institution:
    publications = []
    def __init__(self,name,political_alignment,master_url,publications):
        self.name = name
        self.political_alignment = political_alignment
        self.master_url = master_url
        self.publications = publications

class Publication(Institution):
    def publish(self,title,author,subject,date,url):
        publication_dict = dict(
            title = title,
            author = author,
            subject = subject,
            date = date,
            url = url)
        print publication_dict
        self.publications.append(publication_dict)


'''
base_url = "http://www.think-bank.org/searchform.php?aut=&tit=&top=education"
INSTANTIATE EVERY THINK TANK
'''

heritage_foundation = Institution("Heritage Foundation","Conservative","http://www.heritage.org/issues/education",[])
cato_institute = Institution("Cato Institute","Libertarian","http://www.cato.org/research/education-child-policy",[])
brookings_institution = Institution("Brookings Institution","Centrist","http://www.brookings.edu/",[])
center_for_american_progress = Institution("Center for American Progress","Liberal","http://www.americanprogress.org/issues/education/view/",[])
american_enterprise_institute = Institution("American Enterprise Institute","Conservative","http://www.aei.org/policy/education/",[])
committee_for_economic_development = Institution("Committee for Economic Development","Centrist","http://www.ced.org/policies/education/category/education/",[])
new_america_foundation = Institution("New America Foundation","Centrist","http://education.newamerica.net/dashboard/",[])
pew_research_center = Institution("Pew Research Center","Centrist","http://www.pewresearch.org/topics/education/",[])
rand_corporation = Institution("RAND Corporation","Centrist","http://www.rand.org/topics/education-and-the-arts.html",[])
aspen_institute = Institution("The Aspen Institute","Centrist","http://www.aspeninstitute.org/topics/education",[])
hudson_institute = Institution("The Hudson Institute","Conservative","http://www.hudson.org/topics/12-education",[])
urban_institute = Institution("The Urban Institute","Liberal","http://www.urban.org/education/",[])


'''
page = requests.get(base_url,timeout = 120)
souper = BeautifulSoup(page.content)

listblob = souper.findAll('td')[1].findAll('i')

#print listblob

print len(listblob)

#raw_input()

for numb in range(0,len(listblob)):
    institution = souper.findAll('td')[1].findAll('i')[numb].getText()
    institution = small_clean(institution)
    print institution
    title = souper.findAll('td')[1].findAll('a')[numb].getText()
    print title
    url = souper.findAll('td')[1].findAll('a')[numb].attrs.get('href')
    print url    
    date = souper.findAll('td')[1].findAll('b')[numb+1].getText()
    print date

    raw_input()
'''

