#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPUTING FOR BUSINESS RESEARCH
Homework 2 - Due: October 9th

@author: naa2195, Nolwenn Allaire

    \\_//
    .''\__*
      |   \
      || ||
      
"""

#%%
## Question 1.1:
#Extract at least 10 United Nations press releases containing the word “crisis”. Start with the
#following seed url: https://press.un.org/en. Notice how press release pages have the “PRESS
#RELEASE” relative link in the top left corner. Here is an example press release:
#https://press.un.org/en/2023/sc15431.doc.htm where the “PRESS RELEASE” has the following
#relative anchor tag:
#<a href="/en/press-release" hreflang="en">Press Release</a>
#Use this information to determine whether the web page is a press release.

# Step 1: Import libraries
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

# Step 2: Set up variables
seed_url = "https://press.un.org/en"

seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

pr_urls = []
pr_texts = []
pr_titles = []
pr_html = []

# Step 3: Choose number of URLs to extract (& visit)
pr_count = 0
maxNumUrl = 50; #set the maximum number of urls to visit
maxNumPressRelease = 20; #set the maxmimum number of press releases to extract

# Step 4: Define key words to look for
press_room_un = "/en/press-release"
key_word = "crisis"

# Step 5: Initialize list of URLs to visit
urls = [seed_url]    #queue of urls to crawl

# Step 6: Extract the desired press releases
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if "mailto:" in childUrl: 
            print("Email, irrelevant link")
        else: 
            
            if seed_url in childUrl and childUrl not in seen:
                urls.append(childUrl)
                seen.append(childUrl)
                response = requests.get(childUrl)
                soup = BeautifulSoup(response.content, "html.parser")
                    
                # Check if well press release:
                if soup.find('a', href=press_room_un, hreflang="en") is not None:
                    response = requests.get(childUrl)
                    soup = BeautifulSoup(response.content, "html.parser")
                    element = soup.find(class_="col-md-9 mb-2 panel-panel radix-layouts-main-column") 
                    current_text = element.get_text()
                    
                    # Check if crisis is included in the press release text:
                    if key_word in current_text.lower(): 
                        
                        # Add the URL to the list of urls extracted
                        pr_urls.append(childUrl)
                        
                        global pr_count
                        pr_count += 1
                        
                        # Extract entire html file
                        html = soup.text
                        pr_html.append(html)
                        
                        # Add the text of the press release in list of press releases
                        pr_texts.append(current_text)
                        
                        element2 = soup.find(class_="page-header")
                        title = element2.get_text()
                        # Add title of press release in list of press release titles
                        pr_titles.append(title)
                        if pr_count == maxNumPressRelease+1:
                            break 
                        else: 
                            continue
                    else: 
                        print("######")
                else:
                    print("######")

# Step 7: Save in txt format
for i in range(0,maxNumPressRelease):
    print(pr_urls[i])
    url = pr_urls[i]
    title = pr_titles[i]
    print("\n.Extracted Press Release "+str(title))
    print("\nwith url = "+str(url))
    text_file = open(r'/Users/naa2195/Documents/1st Year/Computing for Business Research/Problem Sets/PS2/to_zip/1_text_'+str(i+1)+'.txt', 'w')
    text_file.write(pr_texts[i])
    text_file.close()
    # Save entire html file
    text_file = open(r'/Users/naa2195/Documents/1st Year/Computing for Business Research/Problem Sets/PS2/to_zip/1_'+str(i+1)+'.txt', 'w')
    text_file.write(pr_html[i])
    text_file.close()
    print("\nPress Release saved in txt format")


#%% 
## Question 1.2:
#Crawl the press room of the European Parliament and extract at least 10 press releases that cover
#the plenary sessions and contain the word “crisis”. Start with the following seed url:
#https://www.europarl.europa.eu/news/en/press-room
#Notice how press releases related to plenary sessions contain the text “PLENARY SESSIONS”
#with the following html:
#<span class="ep_name">Plenary session</span>
#Here is an example:
#https://www.europarl.europa.eu/news/en/press-room/20220620IPR33417/national-recoveryplans-
#meps-assess-the-performance-of-crisis-funding
    
# Step 1: Import libraries
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

# Step 2: Set up variables
seed_url = "https://www.europarl.europa.eu/news/en/press-room"

seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

pr_urls = []
pr_texts = []
pr_titles = []
pr_html = []

# Step 3: Choose number of URLs to extract (& visit)
pr_count = 0
maxNumUrl = 50; #set the maximum number of urls to visit
maxNumPressRelease = 20; #set the maxmimum number of press releases to extract

# Step 4: Define word to look for
key_word = "crisis"

# Step 5: Initialize list of URLs to visit
urls = [seed_url]    #queue of urls to crawl

# Step 6: Extract the desired press releases
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        
        if "hhttps" in childUrl:
            print("Broken link")
        else:
            
            if seed_url in childUrl and childUrl not in seen:
                urls.append(childUrl)
                seen.append(childUrl)
                response = requests.get(childUrl)
                soup = BeautifulSoup(response.content, "html.parser")
                    
                # Check if the page is a press release related to plenary sessions: 
                element = soup.find_all(class_="ep_name")
                ep_names = ""
                for e in element: 
                    e = e.text
                    ep_names += e
                    
                if "Plenary session" in ep_names: 
                    current_text = ""
            
                    # Get the full content of the press release (title, chapo & content of paragraphs)
                    if soup.title and soup.find_all(class_="ep-a_text ep-layout_chapo") and soup.find_all(class_="ep-wysiwig_paragraph") is not None:
                        t = soup.title 
                        title = t.text
                        current_text += title
                        chapo = soup.find_all(class_="ep-a_text ep-layout_chapo")
                        for c in chapo:
                            chap = c.text 
                            current_text += chap
                        paragraphs = soup.find_all(class_="ep-wysiwig_paragraph")
                        for p in paragraphs: 
                            para = p.text
                            current_text += para
                        
                        # Check if crisis is included in the press release text:
                        if key_word in current_text.lower(): 
                                
                            # Add the URL to the list of urls extracted
                            pr_urls.append(childUrl)
                            print(childUrl)
                                
                            global pr_count
                            pr_count += 1
                            
                            # Extract entire html file
                            html = soup.text
                            pr_html.append(html)
                                
                            # Add the text of the press release in list of press releases
                            pr_texts.append(current_text)
                            
                            # Add title of press release in list of press release titles
                            pr_titles.append(title)   
                            if pr_count == maxNumPressRelease+1:
                                break 
                            else: 
                                continue
                        else: 
                            print("######")
                else:
                    print("######")

# Step 7: Save in txt format
for i in range(0,15):
    print(pr_urls[i])
    url = pr_urls[i]
    title = pr_titles[i]
    print("\n.Extracted Press Release "+str(title))
    print("\nwith url = "+str(url))
    # Save text content
    text_file = open(r'/Users/naa2195/Documents/1st Year/Computing for Business Research/Problem Sets/PS2/to_zip/2_text_'+str(i+1)+'.txt', 'w')
    text_file.write(pr_texts[i])
    text_file.close()
    # Save entire html file
    text_file = open(r'/Users/naa2195/Documents/1st Year/Computing for Business Research/Problem Sets/PS2/to_zip/2_'+str(i+1)+'.txt', 'w')
    text_file.write(pr_html[i])
    text_file.close()
    print("\nPress Release saved in txt format")


