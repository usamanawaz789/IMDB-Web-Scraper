import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from pandas.io.html import read_html
import pandas as pd
import html5lib
import csv
# Scrape IMDB for list of movie titles


base_url = 'https://www.imdb.com'
    
#storyline -> plot keywords,genres


#    TO DO:
#details -> country, language ,release date
#Box office ->budget,Cumulative Worldwide Gross
#Company credits -> production co 
#technical specs -> runtime
#cast -> cast original name
#director (h4) -> director
#writer (h4) -> writer
global TitleLst
TitleLst = []
global GenresLst
GenresLst = []
global DirectorLst
DirectorLst = []
global ProducerLst
ProducerLst = []
global WriterLst
WriterLst = []
global CastLst
CastLst = []
global Production_CompaniesLst2
Production_CompaniesLst = []
global Production_CountryLst
Production_CountryLst = []
global Release_DateLst
Release_DateLst = []
global Running_timeLst
Running_timeLst = []
global LanguageLst
LanguageLst = []
global BudgetLst
BudgetLst = []
global BoxOfficeLst
BoxOfficeLst = []

def scrap_page(url):
    

    page = requests.get(url)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    h2 = soup.find_all('h2')
    h3 = soup.find_all('h3')
    #h4 = soup.find_all('h4')
    h4 = soup.find_all('div',class_='see-more inline canwrap')
    details = soup.find_all('div',class_='txt-block')
    casts = soup.find_all('div',class_='article',id='titleCast')[0].find_all('a')


    #child = h4.find('h4')
    maintitle=[]
    plot_keywords = []
    genres = []
    country = []
    revenue=[]
    releasedate = []
    budget = []
    productionco = []
    time_in_minutes=[]
    cast_name=[]
    writers = []
    language = []
    director_name = []

    maintitle.append(soup.find_all('h1')[0].text.split('(')[0].strip())
    director_name.append(soup.find_all('div',class_='credit_summary_item')[0].find_all('a')[0].text)
    writers_a_tag = soup.find_all('div',class_='credit_summary_item')[1].find_all('a')

    for i in writers_a_tag:
        if i.text.replace(' ','').isalpha():
            writers.append(i.text)
    #print(director_name)

    tob=False
    for cast in casts:
        word_length = len(cast.text.replace(' ',''))
        if 'name' in cast.attrs['href'] and word_length > 0:
            cast_name.append(cast.text.strip())

    for item in details:
        if 'Country' in item.text:
            temp = item.find_all('a')
            for a_tag in temp:
                country.append(a_tag.text.strip())
        if 'Language' in item.text:
            temp = item.find_all('a')
            for a_tag in temp:
                language.append(a_tag.text.strip())
        if 'Cumulative Worldwide Gross' in item.text:
            if '$' in item.text:
                revenue.append(item.text.split('$')[1].replace(',','').strip())
        if 'Budget' in item.text:
            if '$' in item.text:
                budget.append(item.text.split('$')[1].replace(',','').split('(')[0].strip())
        if 'Release Date' in item.text:
            if ':' in item.text:
                releasedate.append(item.text.split(':')[1].strip().split('(')[0].strip())
        if 'Production Co' in item.text:
            prods = item.find_all('a')
            for prod in prods:
                if 'see more' not in prod.text.lower():
                    productionco.append(prod.text.strip())
        if 'Runtime' in item.text:
            time_in_minutes.append(item.text.split(':')[1].strip().split(' ')[0])
            
     
    for item in h4:
        if 'Plot Keywords' in item.text:
            temp = item.find_all('span')
            for i in temp:
                if i.text.replace(' ','').isalpha():
                    plot_keywords.append(i.text)
        if 'Genres' in item.text.replace(' ',''):
            temp = item.find_all('a')
            for i in temp:
                if '|' not in i.text:
                    genres.append(i.text.strip())



##    o = {}
##    o['title']=maintitle
##    o['plot_keywords']=plot_keywords
##    o['genre']=genres
##    o['country']=country
##    o['revenue']=revenue
##    o['release_date']=releasedate
##    o['budget']=budget
##    o['productionco']=productionco
##    o['time_in_minutes'] = time_in_minutes
##    o['cast_name']=cast_name
##    o['writers']=writers
##    o['director_name']=director_name
##    
    TitleLst.append(maintitle)
    GenresLst.append(genres)
    DirectorLst.append(director_name)
    WriterLst.append(writers)
    CastLst.append(cast_name)
    Production_CompaniesLst.append(productionco)
    Production_CountryLst.append(country)
    Release_DateLst.append(releasedate)
    Running_timeLst.append(time_in_minutes)
    LanguageLst.append(language)
    BudgetLst.append(budget)
    BoxOfficeLst.append(revenue)

    return TitleLst, GenresLst, DirectorLst, WriterLst, CastLst, Production_CompaniesLst, Production_CountryLst, Release_DateLst, Running_timeLst, LanguageLst, BudgetLst, BoxOfficeLst


#invalid budget url:
#https://www.imdb.com/search/title/?title_type=feature&release_date=1980-01-01,2019-12-31&sort=num_votes,desc&start=7801&ref_=adv_nxt



# Next: https://www.imdb.com/search/title/?title_type=feature&release_date=1980-01-01,2019-12-31&sort=num_votes,desc&after=WzE3NTUsInR0MDA5NDMyMCIsMTcxNTFd
main_url='https://www.imdb.com/search/title/?title_type=feature&release_date=1980-01-01,2019-12-31&sort=num_votes,desc&after=WzE4MjYsInR0MDM2NTgxMCIsMTY4MDFd'
#print(main_page.content)
main_url ='https://www.imdb.com/search/title/?title_type=feature&release_date=1980-01-01,2019-12-31&sort=num_votes,desc&after=WzM0NSwidHQwMTE5OTMwIiwzNzY1MV0%3D'

for i in range(0,1200):

    TitleLst2 = []
    GenresLst2 = []
    DirectorLst2 = []
    ProducerLst2 = []
    WriterLst2 = []
    CastLst2 = []
    Production_CompaniesLst2 = []
    Production_CountryLst2 = []
    Release_DateLst2 = []
    Running_timeLst2 = []
    LanguageLst2 = []
    BudgetLst2 = []
    BoxOfficeLst2 = []

    main_page = requests.get(main_url)
    soup = BeautifulSoup(main_page.content, 'html.parser')
    titles = soup.find_all(class_='lister-item-header')
    next_page_a_tag = soup.find_all(class_='lister-page-next next-page')[0]
    try:
      print(i)
      print(main_url)
      
      for title in titles:
          a_tag = title.find('a')
          temp = base_url+a_tag.attrs['href']
          key = temp.split('/')[len(temp.split('/'))-2]
          
          TitleLst2, GenresLst2, DirectorLst2, WriterLst2, CastLst2, Production_CompaniesLst2, Production_CountryLst2, Release_DateLst2, Running_timeLst2, LanguageLst2, BudgetLst2, BoxOfficeLst2  = scrap_page(base_url+a_tag.attrs['href'])
          #print(TitleLst2)
      movies_df = pd.DataFrame({
      'Name': TitleLst2,
      'Genres': GenresLst2,
      'Director': DirectorLst2,
      'Writer': WriterLst2,
      'Cast': CastLst2,
      'ProductionCompany': Production_CompaniesLst2,
      'ProductionCountry': Production_CountryLst2,
      'ReleaseDate': Release_DateLst2,
      'RunningTIme': Running_timeLst2,
      'Language': LanguageLst2,
      'Budget': BudgetLst2,
      'Revenue': BoxOfficeLst2
      })

      
      print('===============================')
      #print(movies_df.Budget == "[]")
      movies_df = (movies_df[movies_df.astype(str)['Budget'] != '[]'])
      movies_df = (movies_df[movies_df.astype(str)['Revenue'] != '[]'])
      
      print('===============================')
      #movies_df = movies_df[movies_df.Budget != '[]']
      print('===============================')
      #print(movies_df[(movies_df.Budget.len() > 4])
      print('===============================') 
      TitleLst = []
      GenresLst = []
      DirectorLst = []
      ProducerLst = []
      WriterLst = []
      CastLst = []
      Production_CompaniesLst = []
      Production_CountryLst = []
      Release_DateLst = []
      Running_timeLst = []
      LanguageLst = []
      BudgetLst = []
      BoxOfficeLst = []

      export_csv = movies_df.to_csv ('/content/drive/My Drive/ColabNotebooks/DataNew.csv', mode = 'a', header = False)
      main_url = base_url+next_page_a_tag.attrs['href']
      
    except:
        export_csv = movies_df.to_csv ('IMDB Movies Data.csv', mode = 'a', header = False)
      
        main_url = base_url+next_page_a_tag.attrs['href']
        
