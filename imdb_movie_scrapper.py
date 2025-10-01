import selenium
from selenium.webdriver import Safari
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()

url = "https://www.imdb.com/chart/top/"
#create the browser obj
driver = Safari()
#pass the site in the browser obj
driver.get(url)
#add a wait, so the page can fully load up, this way I can retrieve everything, sometimes things might be missing cuz the page hasn't loaded, completely.
time.sleep(5)
#than pass driver.page_source to pass the data in the page
soup = BeautifulSoup(driver.page_source, "html.parser") 
movie_names = soup.select("li h3")
ratings = soup.find_all("span" , attrs = {"data-testid": "ratingGroup--imdb-rating"})
movie_year = soup.find_all("span", attrs = {"class":"sc-15ac7568-7 cCsint cli-title-metadata-item"})

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

#Seperating votes and appending them
for rate in ratings: 
    temp = rate.text
    temp = temp.split()
    votes.append(temp[1])
    rating.append(temp[0])
    
#Seperating movie name and appending them
for num, name in enumerate(movie_names):
    name = re.sub("^[0-9]+.", "", name.text)
    title.append(name)
    number.append(num + 1)

while len(runtime)<len(number):
    runtime.append("0")
    
#Assigning to dataframe columns
df["Movie Number"] = number
df["Movie Name"] = title
df["Released Year"] = years
df["Runtime"] =runtime
df["Rating"] = rating
df["Votes"] = votes

driver.quit()

# Ask the user to select a folder
folder_selected = filedialog.askdirectory()

root.destroy()
root.mainloop()

#Use the selected folder to set the save location
#saving dataframe to csv file
df.to_csv(folder_selected + "/" +"IMDB top 250 movies.csv", index = False)
#prints the file saved location 
print("File saved at\n", folder_selected)

