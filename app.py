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

institution_list = [
    heritage_foundation,
    cato_institute,
    brookings_institution,
    center_for_american_progress,
    american_enterprise_institute,
    committee_for_economic_development,
    new_america_foundation,
    pew_research_center,
    rand_corporation,
    aspen_institute,
    hudson_institute,
    urban_institute]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
    print request.form
    input_to_parse = request.form['input_to_parse']
    for institution in institution_list:
        if str(input_to_parse) == institution.name:
            institution_publications, institution_textblob = think_bank_parser(str(institution.name))
            institution_noun_list, institution_verb_list = keyword_parse(institution_textblob)
            institution_noun_count = pos_counter(institution_noun_list) 
            institution_verb_count = pos_counter(institution_verb_list)

            result_dict = dict(
                noun_count = institution_noun_count[:30],
                verb_count = institution_verb_count[:30])

    return render_template('results.html', data = result_dict)

if __name__ == '__main__':
    app.run(debug=True)
