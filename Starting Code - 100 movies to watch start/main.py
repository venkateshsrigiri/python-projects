import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# This selector works as of the archived snapshot
movie_titles = [tag.getText() for tag in soup.find_all("h3", class_="title")]

# Reverse the list to get 1 to 100
movies = movie_titles[::-1]

# Save to file
with open("movies.txt", "w", encoding="utf-8") as file:
    for movie in movies:
        file.write(f"{movie}\n")