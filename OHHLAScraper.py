# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

import urllib.request
import re
from lxml import html, etree

ohhla = "http://ohhla.com/";
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"]; 

def removeHeader(lyrics):
	#Old RegEx was: r'^Artists:[\w\s.,-:/\\@\'\(\)&\*]*\n'
	subArtists = re.sub(r'^Artist:.*?\n', '', lyrics, flags = re.MULTILINE);
	subArtists2 = re.sub(r'^artist:.*?\n', '', subArtists, flags = re.MULTILINE);
	subAlbum = re.sub(r'^Album:.*?\n', '', subArtists2, flags = re.MULTILINE);
	subAlbum2 = re.sub(r'^album:.*?\n', '', subAlbum, flags = re.MULTILINE);
	subSong = re.sub(r'^Song:.*?\n', '', subAlbum2, flags = re.MULTILINE);
	subSong2 = re.sub(r'^song:.*?\n', '', subSong, flags = re.MULTILINE);
	subTypers = re.sub(r'^Typed by:.*?\n', '', subSong2, flags = re.MULTILINE);
	subTypers2 = re.sub(r'^Typed By:.*?\n', '', subTypers, flags = re.MULTILINE);
	subTypers3 = re.sub(r'^typed by:.*?\n', '', subTypers2, flags = re.MULTILINE);
	subIntro = re.sub(r'^Intro:.*?\n', '', subTypers3, flags = re.MULTILINE);
	subIntro2 = re.sub(r'^intro:.*?\n', '', subIntro, flags = re.MULTILINE);
	return subIntro2;

def removePreLyrics(lyrics):
	subDJ = re.sub(r'\[DJ.*?\].*?\[', '[', lyrics, flags = re.DOTALL);
	subTalking = re.sub(r'-=talking=-.*?\[', '[', subDJ, flags = re.DOTALL);
	subProlouge = re.sub(r'\[Prolouge.*?\].*?\[', '[', subTalking, flags = re.DOTALL);
	subIntros = re.sub(r'\[Intro.*?\].*?\[', '[', subProlouge, flags = re.DOTALL);
	return subIntros;

def removeChorus(lyrics):
	sub10sionnotsinging = re.sub(r'\[10sion not singing\]', '', lyrics);  #Special Case for 10sion lyrics
	subChorus = re.sub(r'\[Chorus\].*?\[', '[', sub10sionnotsinging, flags = re.DOTALL);
	subChorus2 = re.sub(r'Chorus:.*?\[', '[', subChorus, flags = re.DOTALL);
	subChorus3 = re.sub(r'Chorus:.*?(\n{2,})', '', subChorus2, flags = re.DOTALL);
	subChorus4 = re.sub(r'\[Chorus.*?\].*?\[', '[', subChorus3, flags = re.DOTALL);
	subChorus5 = re.sub(r'\[Chorus\] - .*?$', '', subChorus4);
	return subChorus5;

def removeRest(lyrics):
	subNfamous = re.sub(r'\[Nfamous\]\nClap your hands.*?$', '', lyrics, flags = re.DOTALL);  #Special Case for 1200Tech lyrics
	subInterlude = re.sub(r'\[Interlude.*?\].*?\[', '[', subNfamous, flags = re.DOTALL);
	subHook = re.sub(r'\[Hook.*?\].*?\[', '[', subInterlude, flags = re.DOTALL);
	subHookout = re.sub(r'\[Hook.*?\].*?$', '', subHook, flags = re.DOTALL);  # IM NERVOUS THAT THIS WILL CLEAR A WHOLE TEXT ACCIDENTALLY
	subScratchesout = re.sub(r'\[scratches.*?\].*?$', '', subHookout, flags = re.DOTALL);  #I think Special Case for 1982 lyrics
	subOutro = re.sub(r'\[Outro.*?\].*?$', '', subScratchesout, flags = re.DOTALL);
	subTags = re.sub(r'\[.*?\]', '', subOutro);
	subParenths = re.sub(r'\(.*?\)', '', subTags);
	subPartialParens = re.sub(r'\(.*?\n', '', subParenths);
	subPartialParens2 = re.sub(r'^.*?\)\n', '', subPartialParens, flags = re.MULTILINE);
	subCurlys = re.sub(r'\{.*?\}', '', subPartialParens2);
	subQuotes = re.sub(r'\".*?\" - .*?\n', '', subCurlys);
	subQuotes2 = re.sub(r'\".*?\" - .*?$', '', subQuotes);
	subQuotes3 = re.sub(r'\".*?\"\n', '', subQuotes2);
	subQuotes4 = re.sub(r'\".*?\"$', '', subQuotes3);
	subPartialQuotes = re.sub(r'\".+?\n', '', subQuotes4);
	subPartialQuotes2 = re.sub(r'^.+?\"\n', '', subPartialQuotes, flags = re.MULTILINE);
	subComments = re.sub(r'-=.*?=-', '', subPartialQuotes2);
	subScratching = re.sub(r'\*scratching\*.*?\n', '', subComments);
	subScratching2 = re.sub(r'\*scratching\*.*?$', '', subScratching);
	subAstericks = re.sub(r'\*.*?\*', '', subScratching2);
	subAstericks2 = re.sub(r'\*.*?\n', '', subAstericks);
	subChoruses = re.sub(r'^Chorus\n', '', subAstericks2, flags = re.MULTILINE);
	subChoruses2 = re.sub(r'\nChorus$', '', subChoruses);
	subChoruses3 = re.sub(r'\nChorus.*?\n', '', subChoruses2);
	subTimesNum = re.sub(r'x\d+', '', subChoruses3);
	subTimesNum2 = re.sub(r'x \d+', '', subTimesNum);
	subVerse = re.sub(r'Verse.*?:.*?\n', '', subTimesNum2);
	return subVerse;

def cleanNewlines(lyrics):
	subNewline = re.sub(r'\n{2,}', '\n', lyrics);
	return subNewline;

def cleanLyrics(lyrics):
	step1 = removeHeader(lyrics);
	step2 = removePreLyrics(step1);
	step3 = removeChorus(step2);
	step4 = removeRest(step3);
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