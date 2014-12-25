# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

import urllib.request
import re
from lxml import html, etree

ohhla = "http://ohhla.com/";
sites = ["http://ohhla.com/all.html", "http://ohhla.com/all_two.html", "http://ohhla.com/all_three.html", "http://ohhla.com/all_four.html", "http://ohhla.com/all_five.html"]; 

def removeHeader(lyrics):
	subHeader = re.sub(r'^([aA]rtist:|[aA]lbum:|[sS]ong:|[tT]yped [bB]y:|[iI]ntro:).*?\n', '', lyrics, flags = re.MULTILINE);
	return subHeader;

def removePreLyrics(lyrics):
	subPreLyrics = re.sub(r'(\[(DJ|Prolouge|Intro).*?\]|-=talking=-).*?(\n{2,})', '', lyrics);
	subPreLyrics2 = re.sub(r'(\[(DJ|Prolouge|Intro).*?\]|-=talking=-).*?\[', '[', subPreLyrics, flags = re.DOTALL);  #Catches poorly formatted pages
	return subPreLyrics2;

def removeChorus(lyrics):
	sub10sionnotsinging = re.sub(r'\[10sion not singing\]', '', lyrics);  #Special Case for 10sion lyrics
	subChorus = re.sub(r'(\[Chorus.*?\]|Chorus:|Chorus\(.*?\):).*?(\n{2,}|$)', '', sub10sionnotsinging, flags = re.DOTALL);
	subChorus2 = re.sub(r'(\[Chorus.*?\]|Chorus:|Chorus\(.*?\):).*?\[', '[', subChorus, flags = re.DOTALL);  #Catches poorly formatted pages
	return subChorus2;

def removeRest(lyrics):
	subNfamous = re.sub(r'\[Nfamous\]\nClap your hands.*?$', '', lyrics, flags = re.DOTALL);  #Special Case for 1200Tech lyrics
	subNonLyricTags = re.sub(r'(\[(Interlude|Hook|[sS]cratches|Outro).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro:)).*?(\n{2,}|$)', '', subNfamous, flags = re.DOTALL);
	subNonLyricTags2 = re.sub(r'(\[(Interlude|Hook|[sS]cratches|Outro).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro:)).*?\[', '[', subNonLyricTags, flags = re.DOTALL);  #Catches poorly formatted pages
	subTags = re.sub(r'(\[.*?\]|\(.*?\)|\{.*?\}|-=.*?=-)', '', subNonLyricTags2);
	subChorusVerse = re.sub(r'(^Chorus|[vV]erse.*?:).*?(\n|$)', '', subTags, flags = re.MULTILINE);
	subQuotes = re.sub(r'(^\".*?\"( -.*?)*?|(\*scratching\*.*?))(\n|$)', '\n', subChorusVerse, flags = re.MULTILINE); #Subing \n is to preserve the prior line
	subAstericks = re.sub(r'\*.*?(\*|\n)', '', subQuotes); #Seperate expression to not compete with the *scratching* filter
	subPartialParens = re.sub(r'([^\(\n]*?\)|\([^\)\n]*?)(\n|$)', '', subAstericks);
	subPartialQuotes = re.sub(r'(\"[^\"\n]+?|^[^\"\n]+?\")(\n|$)', '\n', subPartialParens, flags = re.MULTILINE);  #Subing \n is to preserve the prior line
	subRepeats = re.sub(r'(x|x )\d+', '', subPartialQuotes);
	return subRepeats;

def cleanCharacters(lyrics):
	subWeirdChar = re.sub(r'(~|\.{2,}|\+)', '', lyrics);  #Leave in -{2,} because of blurred out curse words
	subEndComma = re.sub(r'\b,( )*?\n', '\n', subWeirdChar);
	return subEndComma;

def removeWhitespace(lyrics):
	subSpaces = re.sub(r'^( )+?\b', '', lyrics, flags = re.MULTILINE);
	subEndSpaces = re.sub(r'( )+?\n', '\n', subSpaces);
	subMidSpaces = re.sub(r'( ){2,}', ' ', subEndSpaces);
	subNewline = re.sub(r'\n{2,}', '\n', subMidSpaces);
	return subNewline;

def cleanLyrics(lyrics):
	step1 = removeHeader(lyrics);
	step2 = removePreLyrics(step1);
	step3 = removeChorus(step2);
	step4 = removeRest(step3);
	step5 = cleanCharacters(step4);
	step6 = removeWhitespace(step5);
	return step6;

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
		SpageDom = SpageOpen.read();
		TestAgainst = str(SpageDom);
		if re.match(r'^b[\'\"]<!DOCTYPE.*?>', TestAgainst) is not None:
			SpageHTML = html.fromstring(SpageDom);
			handleSongPage(SpageHTML, myFile);
		else:
			SpageDomUTF = SpageDom.decode("utf-8", "ignore");
			SpageClean = cleanLyrics(SpageDomUTF);
			myFile.write(SpageClean);

def handleSongPage(spage, myFile):
	try:
		lyrics = spage.xpath("//pre/text()")[0];
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