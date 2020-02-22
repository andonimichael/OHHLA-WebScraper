import urllib.request
import re

from lxml import html
from sanitizer import Sanitizer


class OHHLAScraper:
    OHHLA_URL = "http://ohhla.com/"
    ALL_ARTIST_SITES = ["http://ohhla.com/all.html",
                        "http://ohhla.com/all_two.html",
                        "http://ohhla.com/all_three.html",
                        "http://ohhla.com/all_four.html",
                        "http://ohhla.com/all_five.html"]
    TOP_ARTIST_SITES = ["http://ohhla.com/favorite.html"]
    EXCLUDED_ARTISTS = {'113'}

    def __init__(self, output_directory):
        self.output_directory = output_directory
        self.sanitizer = Sanitizer()

    def scrape_all_artists(self):
        for url in self.ALL_ARTIST_SITES:
            self._scrape_all_artists_page(url)

    def scrape_top_artists(self):
        for url in self.TOP_ARTIST_SITES:
            self._scrape_top_artists_page(url)

    def _scrape_all_artists_page(self, url):
        dom = self._extract_dom(url)
        artist_refs = dom.xpath("//pre/a[@href]/@href")

        for artist_ref in artist_refs:
            ref_split = artist_ref.rsplit('/')
            if not artist_ref or self._is_parent_ref(url, artist_ref) or len(ref_split) < 2:
                continue

            artist_name = ref_split[-2]
            if not artist_name or artist_name in self.EXCLUDED_ARTISTS:
                continue

            artist_url = self.OHHLA_URL + artist_ref
            artist_file_name = '{}/{}.txt'.format(self.output_directory, artist_name)

            with open(artist_file_name, 'w') as output_file:
                self._scrape_artist_page(artist_url, output_file)
                output_file.write('\n')

    def _scrape_top_artists_page(self, url):
        dom = self._extract_dom(url)
        artist_refs = dom.xpath("//td/a[@href]/@href")

        for artist_ref in artist_refs:
            artist_name = artist_ref.replace('YFA_', '').replace('.html', '')
            if not artist_name or artist_name in self.EXCLUDED_ARTISTS:
                continue

            artist_url = self.OHHLA_URL + artist_ref
            artist_file_name = '{}/{}.txt'.format(self.output_directory, artist_name)

            with open(artist_file_name, 'w') as output_file:
                self._scrape_top_artist_page(artist_url, output_file)
                output_file.write('\n')

    def _scrape_artist_page(self, url, output_file):
        try:
            dom = self._extract_dom(url)
        except:
            return

        album_refs = dom.xpath("//tr/td/a[@href]/@href")
        for album_ref in album_refs:
            if not album_ref or self._is_parent_ref(url, album_ref):
                continue
            album_url = url + album_ref
            self._scrape_album_page(album_url, output_file)

    def _scrape_album_page(self, url, output_file):
        try:
            dom = self._extract_dom(url)
        except:
            return

        song_refs = dom.xpath("//tr/td/a[@href]/@href")
        for song_ref in song_refs:
            if not song_ref or self._is_parent_ref(url, song_ref):
                continue
            song_url = url + song_ref
            self._scrape_song_page(song_url, output_file)

    def _scrape_top_artist_page(self, url, output_file, recurse=True):
        try:
            dom = self._extract_dom(url)
        except:
            return

        song_refs = dom.xpath("//tr/td/a[@href]/@href")
        for song_ref in song_refs:
            if not song_ref:
                continue
            elif song_ref.endswith('.txt'):
                song_url = self.OHHLA_URL + song_ref
                self._scrape_song_page(song_url, output_file)
            elif song_ref.endswith('html') and recurse:
                next_url = self.OHHLA_URL + song_ref
                self._scrape_top_artist_page(next_url, output_file, recurse=False)

    def _scrape_song_page(self, url, output_file):
        try:
            opened_url = urllib.request.urlopen(url)
            dom = opened_url.read()
        except:
            return

        if re.match(r'^b[\'\"]<!DOCTYPE.*?>', str(dom)) is not None:
            song_html = html.fromstring(dom)
            try:
                lyrics = song_html.xpath("//pre/text()")[0]
            except:
                return
        else:
            lyrics = dom.decode("utf-8", "ignore")

        cleaned_lyrics = self.sanitizer.clean_lyrics(lyrics)
        output_file.write(cleaned_lyrics)
        output_file.write('\n')

    def _is_parent_ref(self, url, ref):
        start_of_relative_ref = len(self.OHHLA_URL) - 1
        end_of_relative_ref = url.rindex('/', 0, len(url) - 1) + 1
        relative_ref = url[start_of_relative_ref:end_of_relative_ref]
        return relative_ref == ref

    @staticmethod
    def _extract_dom(url):
        opened_url = urllib.request.urlopen(url)
        return html.fromstring(opened_url.read())
