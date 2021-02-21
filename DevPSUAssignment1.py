import requests
from bs4 import BeautifulSoup
import json

#Get InfoBox info from Wiki
def getInfoBox(url):

    #Get HTML from URL
    response = requests.get(url)

    #Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find the information card
    box = soup.find("table", {"class": "infobox vcard"})

    #Initilize dict to save info to
    headerTextDict = {'University':box.find('caption').get_text(' ',strip=True)}

    #Checker for last info box data
    websiteReached = False
    #Save header and text in dict
    for tr in box.find_all("tr"):
        
        #Get info box header and text
        head = tr.find('th')
        text = tr.find('td')
        if head != None and text != None and not websiteReached:
            headText = head.get_text(' ',strip=True)
            websiteReached = True if headText == "Website" else False

            #Remove unwanted tags (unless its the website url)
            if not websiteReached:
                for tag in tr(['sup','span','style']):
                    tag.decompose()

            #Add info to lists
            headerTextDict[headText] = text.get_text(' ',strip=True)

    #Return Info in Dict
    return headerTextDict

#sort Dictionary
def sortDict(Dict):
    sortedDict = {}
    for key in sorted(Dict.keys()):
        sortedDict[key] = Dict[key]
    return sortedDict



#Get links of Big10 Teams
def getBig10Links(url = 'https://en.wikipedia.org/wiki/Big_Ten_Conference'):
    response = requests.get(url)

    #Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find the information card
    box = soup.find("table", {"class": "wikitable sortable"})

    #Init list for links
    hrefList = []
    for tr in box('tr'):
        td = tr.find('td') if tr != None else None
        if td != None:
            a = td.find('a')
            hrefList.append('https://en.wikipedia.org'+a.get('href')) if a != None else None

    #Return list of links
    return hrefList

#Finds Big10Links, scrapes infobox, adds to dict, output as json
def toJSON():
    JSONform = {}

    #Find big10 links
    for link in getBig10Links():

        #Get infobox info
        linkInfoBox = getInfoBox(link)
        JSONform[linkInfoBox['University']] = sortDict(linkInfoBox)

    #Sort Dict
    JSONform = sortDict(JSONform)

    #Output to json
    with open('Assignment1output.json', 'w') as json_file:
        json.dump(JSONform, json_file)

#Run main
toJSON()