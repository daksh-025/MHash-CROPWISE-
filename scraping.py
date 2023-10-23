import requests
from bs4 import BeautifulSoup
url = "https://vikaspedia.in/schemesall/schemes-for-farmers"

r = requests.get(url, verify=False)
htmlContent = r.content

soup = BeautifulSoup(htmlContent, 'html.parser')
schemes = soup.find('div', id='texttospeak')

names = soup.find_all('a', class_='folderfile_name')
nameList = []
urlList = []
for name in names[0:5]:
  nameList.append(name.get_text())
  urlList.append("https://vikaspedia.in"+name['href'])
  
descriptions = soup.select("div>p") 
list1= []
for desc in descriptions[0:5]:
  list1.append(desc.get_text())

