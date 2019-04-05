#Importing required libraries
import sys
import urllib
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
# import requests

#Getting the extension out of filename
def findExtension(fileName):
    ext = fileName.split ('.')[-1]
    return ext


#Reading the given webpage
def bsWebpage(url):
    req = Request ( url , headers={'User-Agent': 'Mozilla/5.0'} )
    webpage = urlopen (req).read ()
    soup = BeautifulSoup ( webpage , "html.parser")#.encode("utf-8")
    return soup

#Getting output from from url
def processSite1(url):
    soup = bsWebpage ( url )
    info = soup.find ( 'div' , attrs={'class': 'eed_con'} )
    text = info.text.strip ()
    return text

def processSite2(url):
    soup = bsWebpage ( url )
    info = soup.find('div', attrs={'class': 'infoBox'})
    text = info.text.strip ()
    return text
    
def getApps(url):
    soup = bsWebpage(url)
    z = soup.findAll('table',attrs={'class':'apps'})
    # print(z)
    count = 0
    result = ""
    for l in z:
        j = str(l).split("\n")
        # print(j)
        for m in j:
            try:
                # print(m)
                # print(m,end="  ")
                # print(m.index("</div>"))
                h = m.index("</div>")
                i = m.index("<",h+7)
                result = result +"\t" +m[h+6:i]+"\n"
                # print( m[h+6:i])
                count = count +1
                if count >5:
                    return result
            except:
                pass
    return result

"""
Function to get the Language family.
Call function bsWebpage on the url.
Applying loop to get the requisite output.
"""
def getLanguageFamily(url, ext):
    soup = bsWebpage ( url )
    exts = soup.findAll('td')
    info = ""
    for i in range(len(exts)):
        extention = exts[i].text.strip()
        if(extention == "."+ext.upper()):
            info = exts[i+1].text.strip()
            break
    return info


def findInfo(ext):
    #Obtaining output from source1
    url = "https://fileinfo.com/filetypes/common"
    languageFamily = getLanguageFamily ( url , ext )

    result = ">> Language Family: " + languageFamily
    result += "\n>> Description:\n"

    #Obtaining output from source2
    url1 = "http://www.fileextension.org/" + ext
    result += "\t->Data from FileExtention\n\t" + processSite1 ( url1 )

    #obtaining output from source3
    url2 = "https://fileinfo.com/extension/" + ext
    result += "\n\n\t-> Data from FileInfo\n\t" + processSite2(url2)
    # result.replace("\""," ")
    url3 = "https://FileInfo.com/extension/"+ext
    result +="\n\n>> Compatible Appplication: \n" + getApps(url3)
    return result

# ---------------CODE RUNS FROM HERE----------------
if (len(sys.argv) == 2): #checking if our file is the second variable
    # print(sys.argv[1])
    fileName = sys.argv[1]
    # fileName = "C:\\Users\\Ekam\\Downloads\\test.txt"
    fil = open(fileName,'r').readlines()
    for nam in fil:
        ext = findExtension(nam[:-1])
        result = nam[:-1] + "\n" +findInfo(ext)
        # result = result
        # for ch in result:
        #     print(ch, end=" ")
        print(result)
        print("\n--------------------\n")
else:
    print("NO FILE FOUND") 
    exit(0)