from bs4 import BeautifulSoup
import requests
import toml

url = 'https://arxiv.org/category_taxonomy'

def get_soup(url):
    url = requests.get(url).content
    soup = BeautifulSoup(url,"html.parser")
    return soup

main = get_soup(url).find('div', id='category_taxonomy_list')
cats = main.find_all('h4')

cs_cats = {}

for cat in cats:
    items = cat.text.split()

    symbol = items[0]
    name = ' '.join(items[1:])[1:-1]

    # print(symbol, name)

    if symbol.startswith('cs'):
        cs_cats[symbol] = name

print(toml.dumps(cs_cats))
