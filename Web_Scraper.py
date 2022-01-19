import logging
from bs4 import BeautifulSoup
import requests
import config as cf
from DB_Manager import DB_Manager

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

def go_inside_movie(my_url):
    '''
    Function that receives an URL of the movie page, goes inside it and gets movie name and genres information and then goes
    to the summary/synopsis page of the movie in order to get summaries and synopsis information

    '''

    movie_page = requests.get(my_url)
    movie_soup = BeautifulSoup(movie_page.content, 'html.parser')

    title = movie_soup.find_all(class_ = 'TitleBlock__Container-sc-1nlhx7j-0 hglRHk')[0].find_all('h1')[0].get_text()
    print(title)

    genres_of_movie = movie_soup.find_all(class_='ipc-metadata-list ipc-metadata-list--dividers-all Storyline__StorylineMetaDataList-sc-1b58ttw-1 esngIX ipc-metadata-list--base') \
                [0].find_all('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')

    genres = []
    for genre in genres_of_movie:
        genres.append(genre.get_text())
    genres = ' '.join(genres)

    summaries,synopsis = go_inside_synopsis(movie_soup)

def go_inside_genre(my_url):
    '''
    Function that receives and URL of the main page of movies of one specific genre
    and iterates through the movies there to get the information.

    '''
    genre_page = requests.get(my_url)
    genre_soup = BeautifulSoup(genre_page.content, 'html.parser')
    movie_headers = genre_soup.find_all('h3',class_='lister-item-header')

    for movie_header in movie_headers:
        my_url = movie_header.find_all('a', href=True)[0]
        my_url = 'http://www.imdb.com' + my_url['href']
        go_inside_movie(my_url)
        break


    # print(genre_soup.find_all('h3',class_='lister-item-header'))

def iterate_genre_table(genre_table):
    '''
    Function that receives a beautiful soup tag object with a table with all of the genres and iterates through
    sub tables containing only partial genres of that table.
    For each genre calls the function 'go_inside_genre'.
    '''



    for small_table in genre_table.find_all(class_='table-cell'):
        for genres in small_table.find_all(class_ = 'table-row'):
            genres.find_all(class_='table-cell primary')[0]
            my_url = genres.find_all('a', href=True)[0]
            my_url =  'http://www.imdb.com' + my_url['href']

            go_inside_genre(my_url)
            break
        break

#
#
# # print(tabla_general.find_all(class_='table-cell')[0].prettify())
# tabla_small = tabla_general.find_all(class_='table-cell')[0]
#
# generos = tabla_small.find_all(class_ = 'table-row')
# # print(generos[0].prettify())
#
# aux = 0
# for small_table in tabla_general.find_all(class_='table-cell'):
#     if aux == 1:
#         break
#     for genero in small_table.find_all(class_ ='table-row'):
#         if aux == 1:
#             break
#         genero.find_all(class_='table-cell primary')[0]
#         my_url = genero.find_all('a', href=True)[0]
#         my_url =  'http://www.imdb.com' + my_url['href']
#         print(my_url)
#         aux+=1
#         genre_page = requests.get(my_url)
#         genre_soup = BeautifulSoup(genre_page.content, 'html.parser')
#         # print(genre_soup.prettify())
#
#         movies_in_page = genre_soup.find_all(class_ = 'lister-item mode-advanced')
#         new_url = movies_in_page[0].find_all(class_='lister-item-content')[0].find_all('h3')[0].find_all('a',href=True)[0]
#         new_url = 'http://www.imdb.com' + new_url['href']
#         # print(new_url)
#         movie_page = requests.get(new_url)
#         movie_soup = BeautifulSoup(movie_page.content,'html.parser')
#
#         # print(movie_soup.prettify())
#         content = movie_soup.find_all(class_ = 'ipc-html-content ipc-html-content--base')
#         content = (content[0]).get_text()
#         # print(content)
#
#         genres = movie_soup.find_all(class_='ipc-metadata-list ipc-metadata-list--dividers-all Storyline__StorylineMetaDataList-sc-1b58ttw-1 esngIX ipc-metadata-list--base')\
#         [0].find_all('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
#
#         # for genre in genres:
#         #     print(genre.get_text())
#
#         synopsis_url = movie_soup.find_all(class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline PlotSection__PlotLinks-sc-1hc6syk-0 kSzuBT base')\
#         [0].find_all('li')[1].find_all('a', href=True)[0]
#         synopsis_url = 'http://www.imdb.com' + synopsis_url['href']
#         # print(synopsis_url)
#
#         synopsis_page = requests.get(synopsis_url)
#         synopsis_soup = BeautifulSoup(synopsis_page.content, 'html.parser')
#
#         summaries = synopsis_soup.find_all(id='plot-summaries-content')
#         summaries = summaries[0].find_all('p')
#         # for summ in summaries:
#         #     print(summ.get_text())
#
#         synopsis_content = synopsis_soup.find_all(id='plot-synopsis-content')[0].find_all('li')[0].get_text()
#         # print(synopsis_content)

if __name__ == '__main__':
    # get_genre_table()
    iterate_genre_table(get_genre_table())