# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

import urllib.request
import re
from lxml import html, etree

ohhla = "http://ohhla.com/"
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"]; 


def removeHeader(lyrics):
    subHeader = re.sub(r'^([aA]rtist:|[aA]lbum:|[sS]ong:|[tT]yped [bB]y:).*?\n', '', lyrics, flags = re.MULTILINE)
    subFeatured = re.sub(r'^( |\t)*?f/.*?\n', '', subHeader, flags = re.MULTILINE)
    return subFeatured


def removePreLyrics(lyrics):
    subPreLyrics = re.sub(r'(\[(DJ|Prolouge|Intro|Mr\. Mixx).*?\]|-=talking=-|[iI]ntro:|Note:).*?(\n{2,})', '', lyrics, flags = re.DOTALL);  #Mr. Mixx for 2-Live Crew lyrics
    subPreLyrics2 = re.sub(r'(\[(DJ|Prolouge|Intro).*?\]|-=talking=-).*?\[', '[', subPreLyrics, flags = re.DOTALL);  #Catches poorly formatted pages
    subEquals = re.sub(r'^(\w*?|[^\s\w] [^\s\w]) ?= ?.*?\n', '', subPreLyrics2, flags = re.MULTILINE)
    return subEquals


def removeChorus(lyrics):
    sub10sionnotsinging = re.sub(r'\[10sion not singing\]', '', lyrics);  #Special Case for 10sion lyrics
    subChorus = re.sub(r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?(\n{2,}|$)', '', sub10sionnotsinging, flags = re.DOTALL)
    subChorus2 = re.sub(r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?\[', '[', subChorus, flags = re.DOTALL);  #Catches poorly formatted pages(CHECK IF ALL ARE NEEDED)
    return subChorus2


def removeRest(lyrics):
    subSpecialCases = re.sub(r'(\[Nfamous\]\nClap your hands|\[John Legend\]\nI lay awake|\[Mike Posner\]\nGirl I\'m on that).*?$', '', lyrics, flags = re.DOTALL);  #Special Case for 1200Tech & (2) 2-Chaiz lyrics
    subNonLyricTags = re.sub(r'(\[(Interlude|Hook|[sS]cratches|Outro| OUTRO|[rR]epeat|Breakdown).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro[^\n]*?:|[wW]oman\'s [vV]oice:|Luke[^\n]*?:|Breakdown[^\n]*?:|News [rR]eporter:|BILL[^\n]*?:|Clay D:)).*?(\n{2,}|$)', '', subSpecialCases, flags = re.DOTALL);  #Woman's voice, Luke, Breakdown, News reporter, & BILL: are for 2 Live Crew lyrics
    subNonLyricTags2 = re.sub(r'(\[(Interlude|Hook|[sS]cratches|Outro|[rR]epeat|Breakdown).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro[^\n]*?:|Breakdown[^\n]*?:)).*?\[', '[', subNonLyricTags, flags = re.DOTALL);  #Catches poorly formatted pages
    subTags = re.sub(r'(\[.*?\]|\(.*?\)|\{.*?\}|-=.*?=-)', '', subNonLyricTags2)
    subChorusVerse = re.sub(r'(^Chorus|[vV]erse.*?:|[vV]erse \d+?).*?(\n|$)', '', subTags, flags = re.MULTILINE)
    subAnyColons = re.sub(r'^.*?:(\n|$)', '\g<1>', subChorusVerse, flags = re.MULTILINE)
    subQuotesEtc = re.sub(r'((^( |\t)*?(\".*?\"|\-).*?)|(\*scratching\*.*?))(\n|$)', '\n', subAnyColons, flags = re.MULTILINE); #Subing \n is to preserve the prior line
    subAstericks = re.sub(r'\*.*?(\*|\n)', '\n', subQuotesEtc); #Seperate expression to not compete with the *scratching* filter
    subPartialParens = re.sub(r'(([^\(\n]*?\)|\([^\)\n]*?)|([^\{\n]*?\}|\{[^\}\n]*?)|([^\[\n]*?\]|\[[^\]\n]*?))(\n|$)', '', subAstericks)
    subPartialQuotes = re.sub(r'^((?:[^\"\n]*\"[^\"\n]*\")*[^\"\n]*)\"[^\"\n]*\n[^\"\n]*\"(\n|$)', '\g<1>\n', subPartialParens, flags = re.MULTILINE);  #From StackOverflow
    subPartialQuotes2 = re.sub(r'^[^\"\n]*?\"(\n|$)', '', subPartialQuotes, flags = re.MULTILINE)
    subRepeats = re.sub(r'(x|x )\d+', '', subPartialQuotes2)
    return subRepeats


def cleanCharacters(lyrics):
    subWeirdChar = re.sub(r'(~|\.{2,}|\+|\>|\<|\?(?=[^\n]))', '', lyrics);  #Leave in -{2,} because of blurred out curse words
    subEndings = re.sub(r'(!|\?){2,}', '\g<1>', subWeirdChar);  #Need to check ??? and !?!? cases
    subEndCommaHyph = re.sub(r'(\b,|\-)( |\t)*?(\n|$)', '\n', subEndings)
    return subEndCommaHyph


def removeSingleWords(lyrics):
    subOneWordLine = re.sub(r'^( |\t)*?\S+?( |\t)*?(\n|$)', '', lyrics, flags = re.MULTILINE)
    return subOneWordLine


def removeWhitespace(lyrics):
    subSpaces = re.sub(r'^( |\t)+?(\b|\')', '\g<2>', lyrics, flags = re.MULTILINE)
    subEndSpaces = re.sub(r'( |\t)+?(\n|$)', '\n', subSpaces)
    subMidSpaces = re.sub(r'( |\t){2,}', ' ', subEndSpaces)
    subNewline = re.sub(r'\n{2,}', '\n', subMidSpaces)
    subBegginingLines = re.sub(r'^\n{1,}', '', subNewline)
    subEndingLines = re.sub(r'\n{1,}$', '', subBegginingLines)
    return subEndingLines


def cleanLyrics(lyrics):
    step1 = removeHeader(lyrics)
    step2 = removePreLyrics(step1)
    step3 = removeChorus(step2)
    step4 = removeRest(step3)
    step5 = cleanCharacters(step4)
    step6 = removeSingleWords(step5)
    step7 = removeWhitespace(step6)
    return step7


def handleFrontPage(fpage, base, myFile):
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
        handleArtistPage(ApageDom, url, href, myFile)


def handleArtistPage(apage, base, nextstop, myFile):
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
        handleAlbumPage(AlpageDom, url, nextstop, myFile)


def handleAlbumPage(alpage, base, stop, myFile):
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
            handleSongPage(SpageHTML, myFile)
        else:
            SpageDomUTF = SpageDom.decode("utf-8", "ignore")
            SpageClean = cleanLyrics(SpageDomUTF)
            myFile.write(SpageClean)


def handleSongPage(spage, myFile):
    try:
        lyrics = spage.xpath("//pre/text()")[0]
    except:
        return
    cleanup = cleanLyrics(lyrics)
    myFile.write(cleanup)


def scrapeOHHLA():
    myFile = open("lyrics.txt", "w")
    for url in sites:
        fpageOpen = urllib.request.urlopen(url)
        fpageDom = html.fromstring(fpageOpen.read())
        handleFrontPage(fpageDom, ohhla, myFile)
    myFile.close()


scrapeOHHLA()
