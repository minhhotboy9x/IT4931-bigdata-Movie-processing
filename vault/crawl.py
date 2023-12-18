import requests
from bs4 import BeautifulSoup
import pandas as pd
import collections
from csv import DictWriter
import jsonlines
path = 'results.jsonl'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
cnt = 36000
cnt2 = 37500
list_digit = ['0','1','2','3','4','5','6','7','8','9']
# list_months = {
#     "January": 1,
#     "February": 2,
#     "March": 3, 
#     "April": 4,
#     "May": 5,
#     "June": 6, 
#     "July": 7,
#     "August": 8,
#     "September": 9,
#     "October": 10,
#     "November": 11,
#     "December": 12
# }

with jsonlines.open(path) as reader:
    for obj in reader:
        id = obj['tconst']
        list_res = {}
        print(id)
        url = f'https://www.imdb.com/title/{id}/'
        html = requests.get(url, headers=HEADERS)
        s = BeautifulSoup(html.content, 'html.parser')
        list_res['imdb_id'] = id

        el = s.find('li', attrs={"data-testid":"title-boxoffice-cumulativeworldwidegross"})
        if el is not None:
            string = el.find('span', attrs={"class": "ipc-metadata-list-item__list-content-item", "aria-disabled": "false"}).get_text()
            a = [*string]
            list_res['revenue'] = int("".join([char for char in a if char in list_digit]))

        el = s.find('li', attrs={"data-testid":"title-boxoffice-budget"})
        if el is not None:
            string = el.find('span', attrs={"class": "ipc-metadata-list-item__list-content-item", "aria-disabled": "false"}).get_text()
            a = [*string]
            list_res['budget'] = int("".join([char for char in a if char in list_digit]))

        cnt = 0
        b = ['Director', 'Writers', 'Stars']
        list_res['Director'] = []
        list_res['Writers'] = []
        list_res['Stars'] = []
        for el in s.find_all('ul', attrs={"class":"ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"}):
            for a in el.find_all('a'):
                print(a.get_text())
                list_res[b[cnt]].append(a.get_text())
            cnt += 1
            if cnt == 3:
                break

        el = s.find('span', attrs={"data-testid":"plot-xl", "class":"sc-466bb6c-2 chnFO"})
        if el is not None:
            list_res['summary'] = el.get_text()
        
        
        el = s.find('div', attrs={"data-testid":"storyline-plot-summary", "class":"ipc-overflowText ipc-overflowText--pageSection ipc-overflowText--base"})
        if el is not None:
            a = el.find('div', attrs={"class":"ipc-html-content-inner-div"}).contents
            list_res['storyline'] = a

        el = s.find('li', attrs={"data-testid":"storyline-taglines", "class":"ipc-metadata-list__item ipc-metadata-list-item--link"})
        if el is not None:
            a = el.find('li')
            list_res['taglines'] = a.get_text()
        
        el = s.find('div', attrs={"data-testid":"title-details-section", "class":"sc-f65f65be-0 bBlII"})
        list_companies = []
        list_languages = []
        list_countries = []
        if el is not None:
            for a in el.find_all('a'):
                if 'releaseinfo' in a.get('href'):
                    text = a.get_text()
                    if text == 'Release date' or 'release_date' in list_res:
                        continue
                    # print(text)
                    # text = text.split([" ", ","])
                    # list_res['release_date'] = [int(text[1]), list_months(text[0]), int(text[2])]
                    list_res['release_date'] = text
                if 'country_of_origin' in a.get('href'):
                    list_countries.append(a.get_text())
                if 'company' in a.get('href'):
                    text = a.get_text()
                    if text == 'Production companies':
                        continue
                    list_companies.append(a.get_text())
                if 'primary_language' in a.get('href'):
                    list_languages.append(a.get_text())
            list_res['country_of_origin'] = list_countries
            list_res['production_companies'] = list_companies
            list_res['languages'] = list_languages
        list_res['tconst'] = obj['tconst']
        list_res['originalTitle'] = obj['originalTitle']
        list_res['startYear'] = obj['startYear']
        list_res['runtimeMinutes'] = obj['runtimeMinutes']
        list_res['genres'] = obj['genres']
        with jsonlines.open('final.jsonl', 'a') as writer:
            writer.write(list_res)