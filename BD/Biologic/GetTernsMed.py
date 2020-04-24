import requests
from bs4 import BeautifulSoup

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return root.text

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
                
                 add = []
                 lock = False
                 oneword = False
                 nl = False
                 
                 for word in words.split():
                     if(word[-1] == ","):
                         nl = True
                     else:
                         nl = False
                         
                     word.strip().rstrip(".").rstrip(",")
                     ln = len(word)
                     if(oneword == True and word == "—" and lock == False):
                         lock = True
                     else: 
                         if(ln < 30 and ln > 2 and 
                            chek(word) and lock == False):
                             add.append(word + "\n")
                             oneword = True
                             MT.write(word + " ")
                             if(nl == True):
                                 MT.write("\n")
                                 nl = False
                 if(len(add) > 0):
                     MT.write("\n")
                     for word in add:
                         MT.write(word)
                 if(lock == False and nl == False):
                     MT.write("\n")