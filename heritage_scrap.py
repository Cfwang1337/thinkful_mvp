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