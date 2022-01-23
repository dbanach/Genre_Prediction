# Movie Genre Prediction
**WORK IN PROGRESS**

## Project Description
The idea of the project is to do an NLP Multi Label classification model.   
That is, taking the synopsis of a movie, predict the genres of the movie.  

## Data
The data of the project is data collected though **Web Scraping** from  
[IMDB](www.imdb.com).   
For each movie i collected the following:
>Movie name  
> Summaries  
> Synopsis  
> Genres

Summaries are brief comments about the movie and synopsis is a long   
text (even with spoilers, so be careful) about the movies.

Each movie has one or more different genres associated with it.

This data was saved in an **MYSQL** Database.  

## The Model  
With this information i built an Word2Vec model.

## The Files
