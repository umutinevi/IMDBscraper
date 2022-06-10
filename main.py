import selenium as se
import requests
import bs4 as bs
# TO_DO
# Synapsis pdf save
# excel save
# word_count


url = "https://www.imdb.com/search/title/?genres=sci-fi&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=M77AA9VEQ62R4JE01RNS&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_18"


def get_html(url):
    """
    Get html from url
    """
    response = requests.get(url)
    return response.text


def movie_detail_srape(title_link):
    """
    Scrape movie detail
    """
    response = requests.get("https://www.imdb.com/"+title_link)
    soup = bs.BeautifulSoup(response.text, 'lxml')
    title = soup.select_one("h1[data-testid='hero-title-block__title']").text
    try:
        rating = soup.select_one(
            "div[data-testid='hero-rating-bar__aggregate-rating__score']").text
    except:
        rating = "Not Rated"
    try:
        year = soup.select_one(
            "a[class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh']").text
    except:
        year = "Not Available"
    try:
        genre = soup.select_one(
            "div[data-testid='genres']").text
    except:
        genre = "Not Available"

    synapsis_html = "https://www.imdb.com"+title_link+"plotsummary"
    print(synapsis_html)
    synapsis = get_synapsis(synapsis_html)

    print(title, rating, genre, year, synapsis)


def get_movie_detail_link(html):
    """
    Get movie links
    """
    links = []
    soup = bs.BeautifulSoup(html, 'lxml')
    tiles = soup.find_all('div', class_='lister-item mode-advanced')
    for tile in tiles:
        links.append(
            tile.find('h3', class_='lister-item-header').a.get('href'))
    for link in links:
        movie_detail_srape(link)
    # buraya selenium ile 2.sayfaya geçelim.


def get_synapsis(html):
    """
    Save synapsis
    """
    response = requests.get(html)
    soup = bs.BeautifulSoup(response.text, 'lxml')
    synapsis = soup.find(
        'ul', {"id": "plot-synopsis-content"}).text
    return synapsis


html = get_html(url)
get_movie_detail_link(html)
