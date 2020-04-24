import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import corr
import StemPorter 

def corr_text(text):
    ans = ""
    
    for i in text.splitlines():
        for j in i.split():
            j = StemPorter.Stem(j)
            j = corr.checkWord(j)
            j = j.lower()
            ans += j.strip()
            if(len(j) > 0 and j != " "):
                ans += " "
    return ans

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    
    
    
    return root.text

with open("BD_Med_Sport_Math/Med/Med.txt", "r", encoding = 'utf-8') as inpt:
    cnt = 0
    for ref in tqdm(inpt.readlines()):
        ref = ref.strip()
        text = get_text(ref)
        file = open("BD_Med_Sport_Math/Med/Med_"+str(cnt)+".txt", "w",  encoding = 'utf-8')
        file.write(corr_text(text))
        file.close()
        cnt += 1
        