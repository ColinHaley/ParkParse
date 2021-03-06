from bs4 import BeautifulSoup
import os, requests

from Pushbullet import pushbullet

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        if line[0] == '#':
            continue
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

if __name__ == "__main__":
    thing = pushbullet.PushBullet()
    if(os.environ.get('TARGET_URI')):
        TARGET_URI = os.environ.get('TARGET_URI')
#        print("Targetting: {0}".format(TARGET_URI))
        res = requests.get(TARGET_URI).content
        soup = BeautifulSoup(res,"html.parser")
        text_blocks = soup.find_all("div", "Component text-content-size text-content-style ArticleTextGroup clearfix")

        links_good = 0
        links_bad = 0

        for item in text_blocks[2].find_all("li"):
            if (item.find("a")):
                links_good += 1
            else:
                print(item)
                links_bad += 1
    print ("good: "+ str(links_good))
    print ("bad: "+ str(links_bad))

    if(links_bad < 1):
        thing.send_message(message="Check the glacier link! {0}".format(TARGET_URI), phone_number="+12158402643")
    else:
        print("Message not sent")