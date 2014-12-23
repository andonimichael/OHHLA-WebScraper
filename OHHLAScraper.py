import urllib.request
import re
from lxml import html, etree

ohhla = "http://ohhla.com/";
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"]; 

def removeHeader(lyrics):
	#Old RegEx was: r'^Artists:[\w\s.,-:/\\@\'\(\)&\*]*\n'
	subArtists = re.sub(r'^Artist:.*?\n', '', lyrics, flags = re.MULTILINE);
	subAlbum = re.sub(r'^Album:.*?\n', '', subArtists, flags = re.MULTILINE);
	subSong = re.sub(r'^Song:.*?\n', '', subAlbum, flags = re.MULTILINE);
	subTypers = re.sub(r'^Typed by:.*?\n', '', subSong, flags = re.MULTILINE);
	subTypers2 = re.sub(r'^Typed By:.*?\n', '', subSong, flags = re.MULTILINE);
	return subTypers2;

def removePreLyrics(lyrics):
	subDJ = re.sub(r'\[DJ.*?\].*?\[', '[', lyrics, flags = re.DOTALL);
	subTalking = re.sub(r'-=talking=-.*?\[', '[', subDJ, flags = re.DOTALL);
	return subTalking;

def removeChorus(lyrics):
	sub10sionnotsinging = re.sub(r'\[10sion not singing\]', '', lyrics);  #Special Case for 10sion lyrics
	subChorus = re.sub(r'\[Chorus\].*?\[', '[', sub10sionnotsinging, flags = re.DOTALL);
	subChorus2 = re.sub(r'Chorus:.*?\[', '[', subChorus, flags = re.DOTALL);
	subChorus3 = re.sub(r'Chorus:.*?(\n{2,})', '', subChorus2, flags = re.DOTALL);
	return subChorus3;

def removeTags(lyrics):
	subTags = re.sub(r'\[.*?\]', '', lyrics);
	subComments = re.sub(r'-=.*?=-', '', subTags);
	subTimesNum = re.sub(r'x\d+', '', subComments);
	subTimesNum2 = re.sub(r'x \d+', '', subTimesNum);
	subScratching = re.sub(r'\*scratching\*.*?\".*?\"', '', subTimesNum2, flags = re.DOTALL);
	subAstericks = re.sub(r'\*.*?\n', '', subScratching);
	subChoruses = re.sub(r'Chorus\n', '', subAstericks);
	subChoruses2 = re.sub(r'\nChorus$', '', subChoruses);
	subParenths = re.sub(r'\(.*?\)', '', subChoruses2);
	return subParenths;

def cleanNewlines(lyrics):
	subNewline = re.sub(r'\n{2,}', '\n', lyrics);
	return subNewline;

def cleanLyrics(lyrics):
	step1 = removeHeader(lyrics);
	step2 = removePreLyrics(step1);
	step3 = removeChorus(step2);
	step4 = removeTags(step3);
	step5 = cleanNewlines(step4);
	return step5;

def handleFrontPage(fpage, base, myFile):
	artists = fpage.xpath("//pre/a[@href]/@href");
	for href in artists:
		if href == '':
			continue
		elif href == 'anonymous/113/':	#A French Artist
			continue
		url = base + href;
		try:
			ApageOpen = urllib.request.urlopen(url);
		except:
			continue;
		ApageDom = html.fromstring(ApageOpen.read());
		handleArtistPage(ApageDom, url, href, myFile);

def handleArtistPage(apage, base, nextstop, myFile):
	albums = apage.xpath("//li/a[@href]/@href");
	for href in albums:
		if href == '':
			continue
		elif href == '/anonymous/':
			continue
		url = base + href;
		try:
			AlpageOpen = urllib.request.urlopen(url);
		except:
			continue;
		AlpageDom = html.fromstring(AlpageOpen.read());
		handleAlbumPage(AlpageDom, url, nextstop, myFile);

def handleAlbumPage(alpage, base, stop, myFile):
	currstop = "/" + stop;
	songs = alpage.xpath("//li/a[@href]/@href");
	for href in songs:
		if href == '':
			continue
		elif href == currstop:
			continue
		url = base + href;
		try:
			SpageOpen = urllib.request.urlopen(url);
		except:
			continue;
		SpageDom = html.fromstring(SpageOpen.read());
		handleSongPage(SpageDom, myFile);

def handleSongPage(spage, myFile):
	try:
		lyrics = spage.xpath("//div/pre/text()")[0];
	except:
		return;
	cleanup = cleanLyrics(lyrics);
	myFile.write(cleanup);

def scrapeOHHLA():
	myFile = open("lyrics.txt","w");
	for url in sites:
		fpageOpen = urllib.request.urlopen(url);
		fpageDom = html.fromstring(fpageOpen.read());
		handleFrontPage(fpageDom, ohhla, myFile);
	myFile.close();

scrapeOHHLA();