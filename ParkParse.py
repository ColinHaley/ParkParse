from bs4 import BeautifulSoup
import os, requests

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

if __name__ == "__main__":
    if(os.environ.get('TARGET_URI')):
        TARGET_URI = os.environ.get('TARGET_URI')
        print("Targetting: {0}".format(TARGET_URI))
        res = requests.get(TARGET_URI).content
        soup = BeautifulSoup(res,"html5lib")
        text_blocks = soup.find_all("div", "Component text-content-size text-content-style ArticleTextGroup clearfix")

        links_good = 0
        links_bad = 1

        for item in text_blocks[2].find_all("li"):
            if (item.find("a")):
                links_good +=1

            else:
                links_bad +=1
                print(item)