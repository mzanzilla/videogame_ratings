import requests
import pandas
from bs4 import BeautifulSoup

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

rs = requests.get("https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?sort=desc", headers=headers)

content = rs.content
soup = BeautifulSoup(content, "html.parser")
all = soup.find_all("div", {"class": "product_wrap"})
page_no = soup.find_all("li", {"class": "page"})[-1].text
ls = []
base_url = "https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?sort=desc&page="
for page in range(0, int(page_no)*1, 1):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    print(base_url + str(page))
    rs = requests.get(base_url + str(page), headers=headers)
    content = rs.content
    soup = BeautifulSoup(content, "html.parser")
    all = soup.find_all("div", {"class":"product_wrap"})
    for item in all:
        data = {}
        try:
            data["Title"] = item.find("a").text.replace("\n", " ").replace(" ", "")
            data["Critics Score"]= item.find("div", {"class":"basic_stat product_score brief_metascore"}).text.replace("\n", "")
            data["User Score"]= item.find("li", {"class":"stat product_avguserscore"}).findChildren()[1].text
            data["Release Date"]= item.find("li", {"class":"stat release_date full_release_date"}).findChildren()[1].text
            print(data)
        except:
            None
        ls.append(data)
df = pandas.DataFrame(ls)
df.to_csv("three_month_video_game_ratings.csv")
