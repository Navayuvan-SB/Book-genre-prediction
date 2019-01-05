import urllib2
import ttk
import Tkinter

def geturl():

    txt = open("Genres.txt", "r")
    wr = open("html.txt", "w")
    for x in txt:
        response = urllib2.urlopen(x)
        page = response.read()
        print (page)
        wr.write(page)
        if (True):
            break

    wr.close()
    txt.close()
geturl()