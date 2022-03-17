import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Inform the user that the program is running and that things are loading
print('Obtaining list of squads and their player counts... This should only take a minute.')
print('Speeds are deliberately throttled to place less strain on servers.')
# We're going to define the URL to check as the WB stats page; everything beyond /squads
base_url = 'https://stats.warbrokers.io/squads'
page = requests.get(base_url)  # There's technically no page here
processed_page = BeautifulSoup(page.text, 'html.parser')

squad_urls = list()  # Defining a list for the list of squads to fill
for link in processed_page.find_all('a'):
    if '/squads/' in str(link.get('href')):
        squad_urls.append(str(link.get('href')))

# After gaining a list of all squad links, we'll separate the squad URL portion from the squad name
squad_urls = tqdm([url.replace('/squads/', '') for url in squad_urls]) # setting loading bar up to see progress too
# Read the squad pages to find the number of active players
squad_players = dict()  # numbers will be saved alongside squad name in dictionary
for squad in squad_urls:
    squad_urls.set_description("Counting players in %s" % squad)
    time.sleep(0.1)  # wait for a tenth of a second to restrict program burdening server traffic too much
    page = requests.get(base_url + '/' + squad)
    processed_page = BeautifulSoup(page.text, 'html.parser')
    number_of_players = 0
    for link in processed_page.find_all('a'):  # find the number of player instances
        if '/players/i/' in str(link.get('href')):
            number_of_players += 1
    squad_players[str(squad)] = number_of_players

squad_players = dict(sorted(squad_players.items(), key=lambda x: x[1], reverse=False))  # sort from least to most
print(squad_players)