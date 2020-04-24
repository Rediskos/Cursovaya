import requests
from bs4 import BeautifulSoup

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return root.text

with open("Bio.txt", "w", encoding = "utf-8") as MT:
    with open("BD.txt", "r") as BD:
        #for ref in BD.readlines():
        for i in range(28):
            if (i != 0):
                ref = "https://petroleks.ru/dictionaries/dict_med" + str(i + 1) + ".php"
            else:
                ref = "https://petroleks.ru/dictionaries/dict_med.php"
            text = get_text(ref.strip()).splitlines()
           
            for words in text:
                 add = ""
                 for word in words.split():
                     word.strip()
                     if(word == "—"):
                         MT.write(add)
                     else:
                         add += word + " "