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
from parsers import small_clean, strip_tags, keyword_parse, pos_counter, think_bank_parser

def small_clean(xstr):
    if xstr is None:
        xstr = ""
        return xstr
    else:    
        try:
            xstr=xstr.split(':')[1]
        except:
            pass
        xstr=re.sub(r"\n"," ",xstr)
        xstr=re.sub(r"\r"," ",xstr)
        xstr=re.sub(r"\t"," ",xstr)
        xstr=re.sub(r"`"," ",xstr)
        xstr=re.sub(r"--"," ",xstr)
        xstr=re.sub(r"Information not supplied by college"," ",xstr)
        #xstr = filter(lambda x: x in string.printable, xstr)
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
    def publish(self,title,date,url):
        publication_dict = dict(
            title = title,
            date = date,
            url = url)
        print publication_dict
        self.publications.append(publication_dict)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/education')
def education():
    base_url = "http://www.think-bank.org/searchform.php?aut=&tit=&top=education"

    '''
    INSTANTIATE EVERY THINK TANK
    '''
    heritage_foundation = Institution("Heritage Foundation","Conservative","http://www.heritage.org",[])
    cato_institute = Institution("Cato Institute","Libertarian","http://www.cato.org",[])
    brookings_institution = Institution("Brookings Institution","Centrist","http://www.brookings.edu/",[])
    center_for_american_progress = Institution("Center for American Progress","Liberal","http://www.americanprogress.org/",[])
    american_enterprise_institute = Institution("American Enterprise Institute","Conservative","http://www.aei.org/",[])
    committee_for_economic_development = Institution("Committee for Economic Development","Centrist","http://www.ced.org/",[])
    new_america_foundation = Institution("New America Foundation","Centrist","http://www.newamerica.org/",[])
    pew_research_center = Institution("Pew Research Center","Centrist","http://www.pewresearch.org/",[])
    rand_corporation = Institution("RAND Corporation","Centrist","http://www.rand.org/",[])
    aspen_institute = Institution("The Aspen Institute","Centrist","http://www.aspeninstitute.org/",[])
    hudson_institute = Institution("The Hudson Institute","Conservative","http://www.hudson.org/",[])
    urban_institute = Institution("The Urban Institute","Liberal","http://www.urban.org/",[])

    

    return render_template('education.html')

if __name__ == '__main__':
    app.run(debug=True)
