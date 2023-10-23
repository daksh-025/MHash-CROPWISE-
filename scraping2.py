import requests
from bs4 import BeautifulSoup
url2 = "https://www.nabard.org/content1.aspx?id=23&catid=23&mid=530"
r2 = requests.get(url2, verify=False)
htmlContent2 = r2.content
soup2 = BeautifulSoup(htmlContent2, 'html.parser')
schemes2 = soup2.select("span > ul > li > a")
l2 = []
urlList2 = []
for s in schemes2[0:5]:
  l2.append(s.get_text())
  urlList2.append("https://www.nabard.org/"+s['href'])
print(l2)
print(urlList2)