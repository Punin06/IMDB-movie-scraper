import selenium
from selenium.webdriver import Safari
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

#this displays the top 250 movies on imdb
#remember making the site load completely, by making driver wait before performing queries on it, is paramount.
#data is never missing this way.

url = "https://www.imdb.com/chart/top/"
#create the browser obj
driver = Safari()
#pass the site in the browser obj
driver.get(url)
#add a wait, so the page can fully load up, this way I can retrieve everything, sometimes things might be missing cuz the page hasn't loaded, completely.
time.sleep(5)
#than pass driver.page_source to pass the data in the page
soup = BeautifulSoup(driver.page_source, "html.parser") 
#driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
movie_names = soup.select("li h3")
ratings = soup.find_all("span" , attrs = {"data-testid": "ratingGroup--imdb-rating"})
movie_year = soup.find_all("span", attrs = {"class": "sc-be6f1408-8 fcCUPU cli-title-metadata-item"})

#A count that is used for seperating runtime and released year 
count = 1
#variable to store movie released years
years = []
#this one is to store the runtimes
runtime = []

#A placeholder for the movie year
tyear = ""
#A placeholder for the runtime
temp1 = ""
#stores movies ranking number
number = []
#stores name of movie
title = []
#stores imdb rating of movie
rating = []
#stores imdb number of votes
votes = []
#dataframe to store the movie's number, title, runtime, rating and votes
df = pd.DataFrame()

#seperating the movie released year and runtime, and appending them.
for year in movie_year:
    tyear+=year.text + " "
    if (count%3==0):
        tyear = tyear.split()
        for t in tyear:
            if(re.findall("[0-9]{4}", t)):
                years.append(t)
                
            elif(re.findall("h|m$", t)):
                temp1 += t + " "

            elif not (re.search("([0-9]h.*)|([0-9]+m)|(^[A-Z])", t)):
                runtime.append("N/A")
        
        runtime.append(temp1)
        temp1 = ""
        tyear = ""
    count+=1

#("div", attrs = {"data-testid" : "ratingGroup--container"})

#Seperating votes and appending them
for rate in ratings:
    #t = j.find("span" , attrs = {"data-testid": "ratingGroup--imdb-rating"}).text   
    temp = rate.text
    temp = temp.split()
    votes.append(temp[1])
    rating.append(temp[0])
    
#Seperating movie name and appending them
for num, name in enumerate(movie_names):
    name = re.sub("^[0-9]+.", "", name.text)
    title.append(name)
    number.append(num + 1)

#Assigning to dataframe columns
df["Movie Number"] = number
df["Movie Name"] = title
df["Released Year"] = years
df["Runtime"] =runtime
df["Rating"] = rating
df["Votes"] = votes

#print(df.iloc[[106]]) #Problem here
#print(df.head(25))

driver.quit()

#saving dataframe to csv file
df.to_csv("IMDB top 250 movies.csv", index = False)
    
#from selenium.webdriver.Safari.options import Options
"""

options = Options()
options.headless = True
"""

#when you encounter a moment where you can't scrape with bs4 due to data scraping protection of the website, try passing it in selenium first, then into bs4.
