import re
import time

import requests
from requests import get
from googlesearch import search
response = get('https://natemat.pl/563120,najlepsze-filmy-w-historii-wedlug-widzow-same-filmowe-klasyki-ranking')
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

videos = soup.find_all('h2', class_='c-iQumZg')
regex = r'(^[0-9]+\.) (.*) \(([0-9]{4})\)$'

index_text = "---" + '\n' + "layout: none" + "\n" + "---" + "\n"

index_text = index_text + "# Najlepsze Filmy\n"

for v in videos:
    tytuly = re.findall(regex, v.text)
    time.sleep(5)

    for tytul in tytuly:
        print(tytul[1])
        search_term = tytul[1]

        index_text += "## [" + tytul[0] + " " + tytul[1] + "]" + f"({tytul[0]}md)" + "\n"
        index_text += "Rok produkcji: " + tytul[2] + "\n"

        result = search(f'{tytul[1]} site:pl.wikipedia.org', stop=1, lang="pl")
        url_title = next(result)
        print(url_title)
        response_title = get(url_title)
        soup_title = BeautifulSoup(response_title.text, 'html.parser')

        fabula = soup_title.find('h2', {'id': 'Fabuła'})
        if fabula is None:
            with open(f"{tytul[0]}md", "w", encoding="utf-8") as file:
                file.write(f'[Artykul na wikipedii]({url_title})' + "\n" + "Brak informacji o fabule")
            break

        plot = ("## " + fabula.text +'\n')
        next_element = fabula.find_next('p')
        plot = plot + next_element.text
        while True:
            next_element = next_element.find_next_sibling()
            if next_element.name == 'p':
                plot = plot + next_element.text
            else:
                break

        with open(f"{tytul[0]}md", "w", encoding="utf-8") as file:
            file.write(plot)

with open("index.md", "w", encoding="utf-8") as file:
    file.write(index_text)