#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests 
from bs4 import BeautifulSoup

r= requests.get("https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c=r.content

soup = BeautifulSoup(c,"html.parser")

all = soup.find_all("div" ,{"class" :"propertyRow"})
all[0].find("h4" , {"class" : "propPrice"}).text.replace("\n" , "")


# In[31]:


l=[]
base_url = "https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,30,10):
    r = requests.get(base_url + str(page) + ".html")
    c=r.content
    
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div" ,{"class" :"propertyRow"})
    
    for item in all:
        d={}
        d["Address"]=item.find_all("span" , {"class" , "propAddressCollapse"})[0].text
        d["Locality"]=item.find_all("span" , {"class" , "propAddressCollapse"})[1].text
        d["Price"]=item.find("h4" , {"class" , "propPrice"}).text.replace("\n" , "")

        try:
            d["Beds"]=item.find("span" , {"class" , "infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span" , {"class" , "infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Full Bath"]=item.find("span" , {"class" , "infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"]=None
        try:
            d["Half Bath"]=item.find("span" , {"class" , "infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"]=None
        for column_group in item.find_all("div" ,{"class":"columnGroup"} ):
            #print(column_group)
            for feature_group , feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot size"]=(feature_name.text)
        l.append(d)
        print(l)


# In[33]:


import pandas
df=pandas.DataFrame(l)
print(df)


# In[34]:


df.to_csv("output.csv")

