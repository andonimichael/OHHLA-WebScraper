import urllib.request
import re

from lxml import html
from sanitizer import clean_lyrics


class OHHLAScraper:
    def __init__(self, base_url, front_pages, output_directory):
        self.base_url = base_url
        self.front_pages = front_pages
        self.output_directory = output_directory

    def scrape(self):
        for url in self.front_pages:
            fpageOpen = urllib.request.urlopen(url)
            fpageDom = html.fromstring(fpageOpen.read())
            self._handle_front_page(fpageDom)

    def _handle_front_page(self, fpage):
        artists = fpage.xpath("//pre/a[@href]/@href")
        for href in artists:
            if href == '':
                continue
            elif href == 'anonymous/113/':  # A French Artist
                continue
            url = self.base_url + href
            artist_name = href.rsplit('/')[-2]
            artist_file_name = self.output_directory + '/' + artist_name + '.txt'
            try:
                ApageOpen = urllib.request.urlopen(url)
            except:
                continue
            ApageDom = html.fromstring(ApageOpen.read())

            with open(artist_file_name, 'w') as output_file:
                self._handle_artist_page(ApageDom, url, href, output_file)
                output_file.write('\n')

    def _handle_artist_page(self, apage, base, nextstop, output_file):
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
            self._handle_album_page(AlpageDom, url, nextstop, output_file)

    def _handle_album_page(self, alpage, base, stop, output_file):
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
                self._handle_song_page(SpageHTML, output_file)
            else:
                SpageDomUTF = SpageDom.decode("utf-8", "ignore")
                SpageClean = clean_lyrics(SpageDomUTF)
                output_file.write(SpageClean)
                output_file.write('\n')

    @staticmethod
    def _handle_song_page(spage, output_file):
        try:
            lyrics = spage.xpath("//pre/text()")[0]
        except:
            return
        cleanup = clean_lyrics(lyrics)
        output_file.write(cleanup)
        output_file.write('\n')
