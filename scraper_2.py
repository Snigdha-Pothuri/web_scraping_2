from typing import final                                                                                                    
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time  
import csv
start_url="https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(start_url)    
time.sleep(10)
headers=["Star,Distance,Mass,Radius"]
star_data=[]
new_star_data=[]
def scrap():
    for i in range(1,443):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            current_page_no=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_no<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_no>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break 
        for ul_tag in soup.find_all("ul",attrs={"class","brown_dwarfs"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("") 
            hyper_li_tag=li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyper_li_tag.find_all("a",href=True)[0]["href"])
            star_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")
def scrap_more_data(hyper_link):
    try:
        page=requests.get(hyper_link)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            for i in td_tags:
                try:
                 temp_list.append(i.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyper_link)
scrap()
for index,data in enumerate(star_data):
    scrap_more_data(data[5])
    print(index+1,"page_2_done")
final_star_data=[]
for index,data in enumerate(star_data):
    new_star_data_element=new_star_data[index]
    new_star_data_element=[i.replace("\n","") for i in new_star_data_element()]
    new_star_data_element=new_star_data_element[:7]
    final_star_data.append(data+new_star_data_element)
with open("final.csv","w") as f:
    csv_writer=csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(final_star_data)