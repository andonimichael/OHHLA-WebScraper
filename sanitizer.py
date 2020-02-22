import re


def remove_header(lyrics):
    subHeader = re.sub(r'^([aA]rtist:|[aA]lbum:|[sS]ong:|[tT]yped [bB]y:).*?\n', '', lyrics, flags = re.MULTILINE)
    subFeatured = re.sub(r'^( |\t)*?f/.*?\n', '', subHeader, flags = re.MULTILINE)
    return subFeatured


def remove_pre_lyrics(lyrics):
    subPreLyrics = re.sub(r'(\[(DJ|Prolouge|Intro|Mr\. Mixx).*?\]|-=talking=-|[iI]ntro:|Note:).*?(\n{2,})', '', lyrics, flags = re.DOTALL);  #Mr. Mixx for 2-Live Crew lyrics
    subPreLyrics2 = re.sub(r'(\[(DJ|Prolouge|Intro).*?\]|-=talking=-).*?\[', '[', subPreLyrics, flags = re.DOTALL);  #Catches poorly formatted pages
    subEquals = re.sub(r'^(\w*?|[^\s\w] [^\s\w]) ?= ?.*?\n', '', subPreLyrics2, flags = re.MULTILINE)
    return subEquals


def remove_chorus(lyrics):
    sub10sionnotsinging = re.sub(r'\[10sion not singing\]', '', lyrics);  #Special Case for 10sion lyrics
    subChorus = re.sub(r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?(\n{2,}|$)', '', sub10sionnotsinging, flags = re.DOTALL)
    subChorus2 = re.sub(r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?\[', '[', subChorus, flags = re.DOTALL);  #Catches poorly formatted pages(CHECK IF ALL ARE NEEDED)
    return subChorus2


def remove_rest(lyrics):
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


def clean_characters(lyrics):
    subWeirdChar = re.sub(r'(~|\.{2,}|\+|\>|\<|\?(?=[^\n]))', '', lyrics);  #Leave in -{2,} because of blurred out curse words
    subEndings = re.sub(r'(!|\?){2,}', '\g<1>', subWeirdChar);  #Need to check ??? and !?!? cases
    subEndCommaHyph = re.sub(r'(\b,|\-)( |\t)*?(\n|$)', '\n', subEndings)
    return subEndCommaHyph


def remove_single_words(lyrics):
    subOneWordLine = re.sub(r'^( |\t)*?\S+?( |\t)*?(\n|$)', '', lyrics, flags = re.MULTILINE)
    return subOneWordLine


def remove_whitespace(lyrics):
    subSpaces = re.sub(r'^( |\t)+?(\b|\')', '\g<2>', lyrics, flags = re.MULTILINE)
    subEndSpaces = re.sub(r'( |\t)+?(\n|$)', '\n', subSpaces)
    subMidSpaces = re.sub(r'( |\t){2,}', ' ', subEndSpaces)
    subNewline = re.sub(r'\n{2,}', '\n', subMidSpaces)
    subBegginingLines = re.sub(r'^\n{1,}', '', subNewline)
    subEndingLines = re.sub(r'\n{1,}$', '', subBegginingLines)
    return subEndingLines


def clean_lyrics(lyrics):
    step1 = remove_header(lyrics)
    step2 = remove_pre_lyrics(step1)
    step3 = remove_chorus(step2)
    step4 = remove_rest(step3)
    step5 = clean_characters(step4)
    step6 = remove_single_words(step5)
    step7 = remove_whitespace(step6)
    return step7
