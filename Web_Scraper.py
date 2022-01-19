import logging
from bs4 import BeautifulSoup
import requests
import config as cf
from DB_Manager import DB_Manager
import time

def escape_characters(my_string):
    '''
    Function that receives a string and eliminates the characters ' and " and returns the remaining string.
    '''


    output = my_string.replace("'","")
    output = output.replace('"','')
    return output

def get_genre_table():
    '''
    Function that returns a beautiful soup tag object with a table that contains all of the genres links.
    '''


    page = requests.get(cf.MAIN_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    genre_table = soup.find_all(class_="ab_links")

    genre_table = genre_table[0].find_all(class_='full-table')[0]

    return genre_table

def go_inside_synopsis(movie_soup):
    '''
    Function that receives a beautiful soup tag object and goes into the synopsis/summary page of a movie
    and returns the summaries and the synopsis

    '''



    synopsis_url = movie_soup.find_all(
        class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline PlotSection__PlotLinks-sc-1hc6syk-0 kSzuBT base') \
        [0].find_all('li')[1].find_all('a', href=True)[0]
    synopsis_url = 'http://www.imdb.com' + synopsis_url['href']
    # print(synopsis_url)

    synopsis_page = requests.get(synopsis_url)
    synopsis_soup = BeautifulSoup(synopsis_page.content, 'html.parser')

    summaries = synopsis_soup.find_all(id='plot-summaries-content')
    summaries = summaries[0].find_all('p')
    summary = []
    for summ in summaries:
        summary.append(summ.get_text())
    summary = ' '.join(summary)

    synopsis_content = synopsis_soup.find_all(id='plot-synopsis-content')[0].find_all('li')[0].get_text()

    return summary,synopsis_content

def go_inside_movie(my_url,dbm):
    '''
    Function that receives an URL of the movie page, goes inside it and gets movie name and genres information and then goes
    to the summary/synopsis page of the movie in order to get summaries and synopsis information
    Also receives and passes an object of DB_Manager class in order to interact with the DataBase
    '''

    movie_page = requests.get(my_url)
    movie_soup = BeautifulSoup(movie_page.content, 'html.parser')

    title = movie_soup.find_all(class_ = 'TitleBlock__Container-sc-1nlhx7j-0 hglRHk')[0].find_all('h1')[0].get_text()

    genres_of_movie = movie_soup.find_all(class_='ipc-metadata-list ipc-metadata-list--dividers-all Storyline__StorylineMetaDataList-sc-1b58ttw-1 esngIX ipc-metadata-list--base') \
                [0].find_all('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')

    genres = []
    for genre in genres_of_movie:
        genres.append(genre.get_text())
    genres = ' '.join(genres)

    summaries,synopsis = go_inside_synopsis(movie_soup)

    title = escape_characters(title)
    summaries = escape_characters(summaries)
    synopsis = escape_characters(synopsis)

    dbm.insert(title,summaries,synopsis)

def go_inside_genre(my_url,dbm,count):
    '''
    Function that receives and URL of the main page of movies of one specific genre
    and iterates through the movies there to get the information.
    Receives and passes an object of DB_Manager class in order to interact with the DataBase
    Also receives a counter that's a number that represents how many pages the scraper has moved in one genre.
    '''
    genre_page = requests.get(my_url)
    genre_soup = BeautifulSoup(genre_page.content, 'html.parser')
    movie_headers = genre_soup.find_all('h3',class_='lister-item-header')

    for movie_header in movie_headers:
        my_url = movie_header.find_all('a', href=True)[0]
        my_url = 'http://www.imdb.com' + my_url['href']
        time.sleep(.05)
        go_inside_movie(my_url,dbm)

    print(count)
    if count < cf.PAGES_PER_GENRE:
        time.sleep(.1)
        next_url = (genre_soup.find_all(class_ = 'lister-page-next next-page',href=True)[0])
        next_url = 'http://www.imdb.com' + next_url['href']
        go_inside_genre(next_url,dbm,count+1)



def iterate_genre_table(genre_table,dbm):
    '''
    Function that receives a beautiful soup tag object with a table with all of the genres and iterates through
    sub tables containing only partial genres of that table.
    For each genre calls the function 'go_inside_genre'.
    Also receives and passes an object of DB_Manager class in order to interact with the DataBase
    '''



    for small_table in genre_table.find_all(class_='table-cell'):
        for genres in small_table.find_all(class_ = 'table-row'):
            genres.find_all(class_='table-cell primary')[0]
            my_url = genres.find_all('a', href=True)[0]
            my_url =  'http://www.imdb.com' + my_url['href']

            go_inside_genre(my_url,dbm,1)
            break
        break


if __name__ == '__main__':
    dbm = DB_Manager()
    dbm.build_db()
    iterate_genre_table(get_genre_table(),dbm)
