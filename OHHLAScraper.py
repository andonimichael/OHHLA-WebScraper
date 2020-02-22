# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

import urllib.request
import re
from lxml import html

from sanitizer import clean_lyrics

ohhla = "http://ohhla.com/"
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"];


def handle_front_page(fpage, base, myFile):
    artists = fpage.xpath("//pre/a[@href]/@href")
    for href in artists:
        if href == '':
            continue
        elif href == 'anonymous/113/':	#A French Artist
            continue
        url = base + href
        try:
            ApageOpen = urllib.request.urlopen(url)
        except:
            continue
        ApageDom = html.fromstring(ApageOpen.read())
        handle_artist_page(ApageDom, url, href, myFile)


def handle_artist_page(apage, base, nextstop, myFile):
    albums = apage.xpath("//tr/td/a[@href]/@href")
    for href in albums:
        if href == '':
            continue
        elif href == '/anonymous/':
            continue
        url = base + href
        try:
            AlpageOpen = urllib.request.urlopen(url)
        except:
            continue
        AlpageDom = html.fromstring(AlpageOpen.read())
        handle_album_page(AlpageDom, url, nextstop, myFile)


def handle_album_page(alpage, base, stop, myFile):
    currstop = "/" + stop
    songs = alpage.xpath("//tr/td/a[@href]/@href")
    for href in songs:
        if href == '':
            continue
        elif href == currstop:
            continue
        url = base + href
        try:
            SpageOpen = urllib.request.urlopen(url)
        except:
            continue
        SpageDom = SpageOpen.read()
        TestAgainst = str(SpageDom)
        if re.match(r'^b[\'\"]<!DOCTYPE.*?>', TestAgainst) is not None:
            SpageHTML = html.fromstring(SpageDom)
            handle_song_page(SpageHTML, myFile)
        else:
            SpageDomUTF = SpageDom.decode("utf-8", "ignore")
            SpageClean = clean_lyrics(SpageDomUTF)
            myFile.write(SpageClean)


def handle_song_page(spage, myFile):
    try:
        lyrics = spage.xpath("//pre/text()")[0]
    except:
        return
    cleanup = clean_lyrics(lyrics)
    myFile.write(cleanup)


def scrape_OHHLA():
    myFile = open("lyrics.txt", "w")
    for url in sites:
        fpageOpen = urllib.request.urlopen(url)
        fpageDom = html.fromstring(fpageOpen.read())
        handle_front_page(fpageDom, ohhla, myFile)
    myFile.close()


scrape_OHHLA()
