# OHHLA-WebScraper

This is a simple Web Scraper used to pull lyrics from the [Original Hip-Hop Lyrics Archive](http://ohhla.com/). The lyrics are left out of the github repo because of the extensive size of the archive (and thus the lyrics file). Feel free to clone the repo and run the scraper yourself, but be warned it might take a couple hours to go through all the pages. The OHHLA has a pretty extensive archive.

I intend to use the lyrics with a tweaked version of my Markov Babbler in order to create a Rap Generator. As of 24 Dec. 2014, the regular expressions, used to sanitize the lyrics, need to be improved a bit before this Scraper can be fed to the Markov Model. The sanitization has currently been hand-checked against all lyrics for artist whose names start with a '1' (46 songs with 2300 lines of rap). I intend to hand-test the sanitization will all lyrics for all Artists whose name starts with an integer. There are older entries as well as newer entries to test the sanitization against and will have over 10,000 lines of lyrics which it is tested with. I believe this will be a solid benchmark for the rest of the lyrics in the archive.

Finally, this is my *first ever* program written in Python. Please don't be too harsh judging it, but also **PLEASE** tell me how I butchered Python best practices so I can learn. I literally went from reading the docs to this program. Not a single small test program in between. I also think I did the whole Class/Module thing wrong and in order to execute my file I run 'import OHHLAScraper' which I also think is incorrect. I'm pretty sure any Python expert would cringe at this and re-write it differently. My bad.

-Andoni

## Using the Scraper

1. Download the source code (really just the OHHLAScraper.py file).
2. Start up your Python Command Line (V. 3.2 or higher is guaranteed. Haven't tested on older versions)
3. Execute `import OHHLAScraper`
4. Wait several hours while it compiles a new `lyrics.txt` file for you.

#### Trouble Shooting

Make sure you have the [lxml](http://lxml.de/) library downloaded. The rest of the needed imports are standard in Python3.

## Philosophy Towards Sanitization Rules

Some of you might be upset about what gets sanitized and what stays when going through and parsing the lyrics. There were some major executive calls that needed to be made. Remember, that all of this is intended to be used to feed a Markov Model with the intent of finding rhymes. As such, I excluded all parentheticals, choruses, outros, and the like from the Scraper. All of these sections of lyrics were, for the most part, a break in rhyme-scheme that did not flow with the consistent verses and would not feed nicely into a Markov Model. However, all of these are not to difficult to undo and tweak, in order to make the Scraper fit your own needs.

Some of the decisions cause the loss of rhymes for certain verses (When parentheticals indicated a background voice completing the rhyme), but on the larger picture it was necessary to lose these couple of rhymes in order to preserve the sanitization for the rest of the poorly formatted archive of lyrics.

**UPDATE** (24 Dec. 2014): Thanks to the wonderful and brilliant minds on Stack Overflow, I am now able to exclude Chorus blocks at the end of a page as well! Further, some playing around with alternations helped to clean up the Regular Expressions a ton. Finally, some inginuity and creativity managed to fix the Partial-Parentheses/Partial-Quotes bugs!

Currently, there are three known bugs:
1. For some reason *smart* or *curly* quotes get dropped with lxml's html fromstring function. Instead of being converted into *straight* or *dumb* quotes, they are dropped completely. This makes stray phrases in pages such as [this](http://ohhla.com/anonymous/1st_infa/rm_bside/fourthof.1st.txt) escape my quote-sanitization. It's a slightly annoying bug that is slightly out of my current focus with this project. We'll see if I resolve it or if it is trivial enough that I let those few lines slide.
2. I discovered that the Web Scraper skipped a few albums and a song of 2-chainz. I have only tested up to 2-hungry right now, and 2-chainz was the only example of the Web Scraper missing albums or songs of any artist. Weird. I'll look into the page's hrefs and stuff tomorrow to see whose end the problem is on.
3. Handling quotes is not perfect. Quotes in sentences get deleted (not my intention). AND when they get deleted, it bumps up the previous line. I need to add a '^' to the beginning of the Regex and instead of substitution an empty string, substitute a newline. Tomorrow I will also check the backwards compatibility of this fix to ensure everything else maintains its current quality.

If you have any questions or strong feelings towards excluding (or including) sanitizations of the lyrics, feel free to email me at [andoni@uchicago.edu](mailto:andoni@uchicago.edu).
