from flask import Flask, render_template, request
import re
import os
import nltk
from bs4 import BeautifulSoup
import numpy
import collections

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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/education')
def education():
    source_url = "http://www.think-bank.org/searchform.php?aut=&tit=&top=education"

    '''
    INSTANTIATE EVERY THINK TANK
    '''

    return render_template('education.html')

if __name__ == '__main__':
    app.run(debug=True)
