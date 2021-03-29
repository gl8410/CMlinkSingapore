from selenium import webdriver
import string
import zipfile
import time
import re
import os
import csv
import pygame
from selenium.webdriver import ActionChains

# Define settings to proxy server
proxyHost="http-dyn.abuyun.com"
proxyPort="9020"
proxyUser="guilin8410"
proxyPass="kg@1odifueowt7iosidf#41oisadf"

# Define target website to visit
cmLink="https://www.cmlink.com/sg/"
promotionCode=""
cnNumber="xxxxxxxx9900"
numberpath="numbers.csv"
musicPath="boss.mp3"

# Define patterns you want
#patterns=[r'00\b',r'99\b',r'1984\b',r'8410\b',r'0112\b',r'0104\b',r'1006\b']
patterns=[r'8410\b',r'9900\b',r'0099\b',r'5\b']

def store2CSV(path, line):
    if os.path.isfile(path):
        with open(path, mode="a+", encoding="utf-8", newline="") as f:
            fcsv = csv.writer(f, delimiter=",")
            fcsv.writerow(line)
    else:
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            fcsv = csv.writer(f, delimiter=",")
            fcsv.writerow(line)

def playMusic(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

def getCmlinkNumbers(url):
    while True:
        driver=webdriver.Edge()
        #driver.minimize_window()
        try:
            driver.get(url)
            time.sleep(1.7)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-3200);")
            time.sleep(1.5)
            plan=driver.find_element_by_xpath('//a[contains(text(),"CHOOSE")]')
            time.sleep(1.2)
            plan.click()
            time.sleep(1.6)
            plan20 = driver.find_element_by_xpath('//div[@class="packageBox"][1]//span[contains(@class,"price")]')
            time.sleep(1.2)
            plan20.click()
            # promotion=driver.find_element_by_xpath('//input[contains(@placeholder,"Promotion")]')
            # promotion.send_keys(promotionCode)
            # cnnumber=driver.find_element_by_xpath('//input[contains(@placeholder,"China")]')
            # cnnumber.send_keys(cnNumber)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            time.sleep(1.7)
            go=driver.find_element_by_xpath('//a[contains(@class,"btn greenLineBtn")]')
            time.sleep(1.2)
            go.click()
            time.sleep(1.8)
            # action=ActionChains(driver)
            # action.move_to_element(go)
            # time.sleep(2)
            # action.click()
            # action.perform()
            #ActionChains(driver).move_to_element(go)
            #go.click()
            # go = driver.find_element_by_xpath('//a[contains(@class,"btn greenLineBtn")]')
            numberbtn = driver.find_element_by_xpath('//i[contains(@class,"redArrow")]/..')
            time.sleep(1.6)
            numberbtn.click()
            time.sleep(1.3)
            numlist=get2X(driver,'//div[@id="numberWrap"]//div[@class="optionValue"]')
            print(f"Find numbers: {0}", numlist)
            t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            numlist.insert(0,t)
            store2CSV(numberpath, numlist)
            if meetNumber(numlist,patterns):
                playMusic(musicPath)
                choic=input("Continue? y/n")
                if choic == "n":
                    break
        finally:
            driver.close()
            driver.quit()

def meetNumber(nlist,patterns):
    stop=False
    for n in nlist:
        for p in patterns:
            if re.search(p,n):
                stop=True
    return stop

def get2X(dr, regax):
    name = []
    try:
        names = dr.find_elements_by_xpath(regax)
        for n in names:
            if n.text != "":
                name.append(n.text)
        return name
    except:
        return name


def findElement(dr, regax):
    try:
        dr.find_element_by_xpath(regax)
        return True
    except:
        return False

def createProxyAuth(host,port,user,pwd,scheme="http",pluginpath=None):
    if pluginpath is None:
        pluginpath=r'./{}_{}http-dyn.abuyun.com_9020.zip'.format(user, pwd)
    manifestjs="""{
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Abuyun Proxy",
        "permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>",
                        "webRequest","webRequestBlocking"],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }
    """
    backgroundjs=string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=host,
        port=port,
        username=user,
        password=pwd,
        scheme=scheme
    )
    with zipfile.ZipFile(pluginpath,'w') as zp:
        zp.writestr("manifest.json",manifestjs)
        zp.writestr("background.js",backgroundjs)
    return pluginpath

if __name__=="__main__":

#    proxyAuthPlugingPath=createProxyAuth(host=proxyHost,port=proxyPort,user=proxyUser,pwd=proxyPass)
#    option=webdriver.ChromeOptions()
#    option.add_argument("--start-maximized")
#    option.add_extension(proxyAuthPlugingPath)
    getCmlinkNumbers(cmLink)

