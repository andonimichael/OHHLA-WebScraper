import urllib.request
import re
from lxml import html, etree

ohhla = "http://ohhla.com/";
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"]; 

def handleFrontPage(fpage, base, myFile):
	artists = fpage.xpath("//pre/a[@href]/@href");
	for href in artists:
		if href == '':
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
	subArtists = re.sub(r'^Artist:[\w\s.,-:/\\@\'\(\)]*', '', lyrics, flags = re.MULTILINE);
	subAlbum = re.sub(r'^Album:[\w\s.,-:/\\@\'\(\)]*', '', subArtists, flags = re.MULTILINE);
	subSong = re.sub(r'^Song:[\w\s.,-:/\\@\'\(\)]*', '', subAlbum, flags = re.MULTILINE);
	subTyper = re.sub(r'^Typed by:[\w\s.,-:/\\@\'\(\)]*', '', subSong, flags = re.MULTILINE);
	subTags = re.sub(r'\[.*?\]','',subTyper);
	subComments = re.sub(r'\(.*?\)','',subTags);
	subNotes = re.sub(r'-=.*?=-','',subComments);
	subStars = re.sub(r'\*.*?\*','',subNotes);
	subDblStars = re.sub(r'\*\*[\w\s.-:/\\@\'\(\)]*','',subStars, flags = re.MULTILINE);
	subCleanup = re.sub(r'\n{2,}','\n',subDblStars);
	myFile.write(subCleanup);

def scrapeOHHLA():
	myFile = open("lyrics.txt","w");
	for url in sites:
		fpageOpen = urllib.request.urlopen(url);
		fpageDom = html.fromstring(fpageOpen.read());
		handleFrontPage(fpageDom, ohhla, myFile);
	myFile.close();

scrapeOHHLA();