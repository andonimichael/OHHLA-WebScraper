# OHHLA-WebScraper

There are two parts to this Web Scraper. First, there is a nice and simple Web Scraper used to pull lyrics from the [Original Hip-Hop Lyrics Archive](http://ohhla.com/). Second, there is an extensive amount of sanitization and filtering of the lyrics.

My use of the scraper is to have a file of rap verses (hopefully with a high percentage of rhyming lines), and as such, I needed to filter out a lot of the background noise, so to say, in each song.  Feel free to tweak the scraper and tailor it for you -- you can keep the artists, song names, albums and other meta-data, chorus info, etc. depending on what suits your needs.  I wanted to make this as an easy way to just get a collection of rap verses, but if you want to add bells and whistles, it will only take a few small easy changes!

The lyrics are left out of the github repo because of the extensive size of the archive. Feel free to clone the repo and run the scraper yourself, but be warned it might take several hours to go through all the pages. The OHHLA has a pretty extensive archive and my dirty (but pretty comprehensive) approach to sanitization with a bunch of regular expressions is not too efficient (Currently around 75,000 lines of lyrics/10 mins).

I intend to use the lyrics with a tweaked version of my Markov Babbler in order to create a Rap Generator. As of 28 Dec. 2014, the regular expressions, used to sanitize the lyrics, need to be improved a bit before this Scraper can be fed to the Markov Model. The sanitization has currently been hand-checked against all lyrics for artist up through 2 Low (175 songs with 7500 lines of rap). I intend to hand-test the sanitization will the lyrics for all artists whose name starts with a 1 or 2. There are older entries (1200 Techniques) as well as newer entries (2 Chainz) to test the sanitization against and will have over 10,000 lines of lyrics which it is tested with. I believe this will be a solid benchmark for the rest of the lyrics in the archive.

Finally, this is my *first ever* program written in Python. Please don't be too harsh judging it, but also **PLEASE** tell me how I butchered Python best practices so I can learn. I literally went from reading the docs to this program. Not a single small test program in between.

-Andoni

## Using the Scraper

1. Download the source code (really just the OHHLAScraper.py file).
2. Start up your Python Command Line (V.3.2 or higher is guaranteed. Haven't tested on older versions)
3. Execute `import OHHLAScraper`
4. Wait several hours while it compiles a new `lyrics.txt` file for you.

#### Trouble Shooting

Make sure you have the [lxml](http://lxml.de/) library downloaded. The rest of the dependencies are standard in Python3.

## Philosophy Towards Sanitization Rules

Some of you might be upset about what gets sanitized and what stays when going through and parsing the lyrics. There were some major executive calls that needed to be made. Remember, that all of this is intended to be used to feed a Markov Model with the intent of finding rhymes. As such, I excluded all parentheticals, choruses, outros, and the like from the Scraper. All of these sections of lyrics were, for the most part, a break in rhyme-scheme that did not flow with the consistent verses and would not feed nicely into a Markov Model. However, all of these are not to difficult to undo and tweak, in order to make the Scraper fit your own needs.

Some of the decisions cause the loss of rhymes for certain verses (When parentheticals indicated a background voice completing the rhyme), but on the larger picture it was necessary to lose these couple of rhymes in order to preserve the sanitization for the rest of the poorly formatted archive of lyrics. Also, I recently decided to remove single-word sentences because almost every instance correlated with an interjection or poorly formatted parentheticals that escaped my sanitization efforts.

**UPDATE** (25 Dec. 2014): I just made a pretty dirty hack that fixes the bug with skipped albums and songs (Mostly 2-chainz and ALL due to bad formatting of the XHTML page). It's not pretty, but its functional -- for now. It appears that some pages, such as [this](http://ohhla.com/anonymous/2_chainz/BOATS_2/36.2cz.txt) have incorrectly formatted XHTML head's. Clearly the head is pretty blank, so when it gets loaded by the urllib request and then broken into a stringed format, it only includes the text of the pre-element. As such, lxml's html parser reads it, finds no html and returns a blank document. This then causes it to look like the pages are missing completely. I had to split the urllib opened pages into properly formatted or not. Then I just directly handle the decoded (utf-8, ignore) string of the imporperly formatted pages and handle the others as usual.

Currently, there are two known bugs:

1. For some reason *smart* or *curly* quotes get dropped with lxml's html fromstring function. Instead of being converted into *straight* or *dumb* quotes, they are dropped completely. This makes stray phrases in pages such as [this](http://ohhla.com/anonymous/1st_infa/rm_bside/fourthof.1st.txt) escape my quote-sanitization. It's a slightly annoying bug that is slightly out of my current focus with this project. We'll see if I resolve it or if it is trivial enough that I let those few lines slide.
2. During my aforementioned hack to read from all the pages on the OHHLA, I was forced to include the `"ignore"` flag with the utf-8 decoding. This is because [some](http://ohhla.com/anonymous/2_chainz/BOATS_2/feds_wat.2cz.txt) pages have unique characters (like the French ç), which cause the decoder to throw an error. I will look into other encodings, but for now UTF-8 requires me to lose some letters occasionally (because of the included ignore flag).
3. Partial quotes still are not perfectly situated. If there is an odd number of quotes (i.e. a partial quote that did not have an end-quote), my expression will not be able to evaluate it.

If you have any questions or strong feelings towards excluding (or including) sanitizations of the lyrics, feel free to email me at [andoni@uchicago.edu](mailto:andoni@uchicago.edu).
