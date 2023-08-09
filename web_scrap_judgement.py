# %%
# Load selenium components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time, os

"""
for Linux, do these commands before using webdriver:
    cd /usr/local/share
    wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
    ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

for windows, to use the webdriver
    download from https://chromedriver.chromium.org/
    unzip the exe into the working folder
    done
"""

# %%
urls = {
    "FinalAppeal_Criminal_2021": "https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FA&L2=CC&L3=2021&AR=2_2#A2_2", 
    "FinalAppeal_Criminal_2022": "https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FA&L2=CC&L3=2022&AR=2_1#A2_1",
    "DistrictCourt_CriminalCase_2021": "https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=DC&L2=CC&L3=2021&AR=2_2#A2_2",
    "DistrictCourt_CriminalCase_2022": "https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=DC&L2=CC&L3=2022&AR=2_1#A2_1"
}

# %%
driver = webdriver.Chrome()

# loop the url list (for judgement only)
for l in urls:    
    print("now doing",l)

    # get url for scrapping
    url = urls[l]

    # open url in browser
    driver.get(url)

    # search and get a list document links as elements
    elems = driver.find_elements(By.XPATH,"//*[@id='JSCookTreeItem']/td[3]/a/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a")
    print("found",elems.__len__(),"elements")
    
    # setting download path
    dl_path = os.path.join(os.getcwd(), l)

    # create folder if not exist
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
        print("created path",dl_path)

    # tell the browser to download to designated location and open a new window
    option = webdriver.ChromeOptions()
    option.add_experimental_option("prefs", {"download.default_directory" : dl_path})
    driver2 = webdriver.Chrome(options=option)

    # loop the element lists to get the link
    for e in elems:
        try:
            # get href link from elements, extract the exact url we need, then replace "frame" with "top" to only get the document download link
            # this is because the "frame" link will open a page with several frames, we only need the top frame
            link = e.get_attribute("href").partition("('")[2].partition("%27")[0].replace("frame","top")
            print("find",link)
            # open the extracted link
            driver2.get(link)
            #find the "Go to Word" element and click it to download it
            driver2.find_element(By.XPATH, "/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[1]/a[3]").click()
            time.sleep(1)
        except:
            print("cannot get href")

    time.sleep(2)
    driver2.close()

    print("finish all elements")
    time.sleep(3)
driver.close()
    


