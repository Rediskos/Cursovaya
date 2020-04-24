import requests
from bs4 import BeautifulSoup

def get_text(url):
    rs = requests.get(url)

    return rs.text

allowed = [" "]
disallowed = ["(", "{", "<", "/",
              "^", "\\", "_", '"', "}", ")",
              "[", "]", "×" ,"#", ".", "%","∠",";"]

def chek(word):
    for i in word:
        if i in disallowed:
            return False
        
    return True

with open("tmp.txt", "w", encoding = "utf-8") as MT:
    with open("BD.txt", "r", encoding = "utf-8") as BD:
        for ref in BD.readlines():
            l = "https://ru.wikipedia.org/w/index.php?title="
            r = "&printable=yes"
            t = l + ref.replace(" ", "_").strip() + r
            print(t)
                
            ref = t.strip()
            text = get_text(ref.strip()).splitlines()
           
            for words in text:
                k = words.split()
                if(len(k) > 0 and len(k[0]) > 7):
                    t = k[0]
                    t = t.replace("<li><b>", "").replace("</b>", "")
                    MT.write(t + "\n")