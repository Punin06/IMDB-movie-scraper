import selenium
from selenium.webdriver import Safari
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

#this displays the top 250 movies on imdb

def main():
    url = "https://www.imdb.com/chart/top/"
    #create the browser obj
    driver = Safari()
    #pass the site in the browser obj
    driver.get(url)
    #adding a wait, so the page can fully load up.
    time.sleep(5)
    #creating soup obj using driver page source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #selecting all the movie's names
    movie_names = soup.select("li h3")
    #finding all the movie's ratings
    ratings = soup.find_all("span" , attrs = {"data-testid": "ratingGroup--imdb-rating"})
    #finding all the movie's released year
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

                elif not (re.search("(^[A-Z])", t)):
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

    #Assigning to dataframe columns
    df["Movie Ranking"] = number
    df["Movie Name"] = title
    df["Released Year"] = years
    df["Runtime"] =runtime
    df["Rating"] = rating
    df["Votes"] = votes

    driver.quit()

    print("Saving data to IMDB top 250 movies.csv")
    #saving dataframe to csv file
    df.to_csv("IMDB top 250 movies.csv", index = False)
    print("Data Saved, now displaying entries!")
    file = pd.read_csv("IMDB top 250 movies.csv", sep = ",")
    num_of_movies = int(input("Enter number of top movies to show!\n"))
    pd.set_option("display.max_columns", None)
    print(file.head(num_of_movies))
        

if __name__ =="__main__":
    main()
    
