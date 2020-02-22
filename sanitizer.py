import re


class Sanitizer:
    def clean_lyrics(self, lyrics):
        step1 = self._remove_header(lyrics)
        step2 = self._remove_pre_lyrics(step1)
        step3 = self._remove_chorus(step2)
        step4 = self._remove_rest(step3)
        step5 = self._clean_characters(step4)
        step6 = self._remove_single_words(step5)
        step7 = self._remove_whitespace(step6)
        return step7

    def _remove_header(self, lyrics):
        if not hasattr(self, 'header_re'):
            self.header_re = re.compile(r'^([aA]rtist:|[aA]lbum:|[sS]ong:|[tT]yped [bB]y:).*?\n', flags=re.MULTILINE)
            self.featured_re = re.compile(r'^( |\t)*?f/.*?\n', flags=re.MULTILINE)

        header_removed = re.sub(self.header_re, '', lyrics)
        featured_removed = re.sub(self.featured_re, '', header_removed)
        return featured_removed

    def _remove_pre_lyrics(self, lyrics):
        if not hasattr(self, 'prelyrics_re'):
            self.prelyrics_re = re.compile(
                r'(\[(DJ|Prolouge|Intro|Mr\. Mixx).*?\]|-=talking=-|[iI]ntro:|Note:).*?(\n{2,})',
                flags=re.DOTALL) # Mr. Mixx for 2-Live Crew lyrics
            self.prelyrics2_re = re.compile(r'(\[(DJ|Prolouge|Intro).*?\]|-=talking=-).*?\[',
                                            flags=re.DOTALL)  # Catches poorly formatted pages
            self.equals_re = re.compile(r'^(\w*?|[^\s\w] [^\s\w]) ?= ?.*?\n', flags=re.MULTILINE)

        prelyrics_removed = re.sub(self.prelyrics_re, '', lyrics)
        prelyrics2_removed = re.sub(self.prelyrics2_re, '[', prelyrics_removed)
        equals_removed = re.sub(self.equals_re, '', prelyrics2_removed)
        return equals_removed

    def _remove_chorus(self, lyrics):
        if not hasattr(self, 'sub10sionnotsinging_re'):
            self.sub10sionnotsinging_re = re.compile(r'\[10sion not singing\]')
            self.chorus_re = re.compile(
                r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?(\n{2,}|$)',
                flags=re.DOTALL)
            self.chorus2_re = re.compile(
                r'(\[(Chorus| CHORUS)[^\n]*?\]|Chorus:|Chorus( |\t)*?(\([^\n]*?\)|\{[^\n]*?\}):).*?\[',
                flags=re.DOTALL)

        sub10sionnotsinging_removed = re.sub(self.sub10sionnotsinging_re, '', lyrics)
        chorus_removed = re.sub(self.chorus_re, '', sub10sionnotsinging_removed)
        chorus2_removed = re.sub(self.chorus2_re, '[', chorus_removed)
        return chorus2_removed

    def _remove_rest(self, lyrics):
        if not hasattr(self, 'specialcases_re'):
            self.specialcases_re = re.compile(
                r'(\[Nfamous\]\nClap your hands|\[John Legend\]\nI lay awake|\[Mike Posner\]\nGirl I\'m on that).*?$',
                flags=re.DOTALL) # Special Case for 1200Tech & (2) 2-Chaiz lyrics
            self.nonlyrictags_re = re.compile(
                r'(\[(Interlude|Hook|[sS]cratches|Outro| OUTRO|[rR]epeat|Breakdown).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro[^\n]*?:|[wW]oman\'s [vV]oice:|Luke[^\n]*?:|Breakdown[^\n]*?:|News [rR]eporter:|BILL[^\n]*?:|Clay D:)).*?(\n{2,}|$)',
                flags=re.DOTALL) # Woman's voice, Luke, Breakdown, News reporter, & BILL: are for 2 Live Crew lyrics
            self.nonlyrictags2_re = re.compile(r'(\[(Interlude|Hook|[sS]cratches|Outro|[rR]epeat|Breakdown).*?\]|(Interlude:|Hook:|[sS]cratches:|Outro[^\n]*?:|Breakdown[^\n]*?:)).*?\[',
                                               flags=re.DOTALL) # Catches poorly formatted pages
            self.tags_re = re.compile(r'(\[.*?\]|\(.*?\)|\{.*?\}|-=.*?=-)')
            self.chorusverse_re = re.compile(r'(^Chorus|[vV]erse.*?:|[vV]erse \d+?).*?(\n|$)', flags=re.MULTILINE)
            self.colons_re = re.compile(r'^.*?:(\n|$)', flags=re.MULTILINE)
            self.quotes_re = re.compile(r'((^( |\t)*?(\".*?\"|\-).*?)|(\*scratching\*.*?))(\n|$)', flags=re.MULTILINE)
            self.asterisks_re = re.compile(r'\*.*?(\*|\n)')
            self.partialparens_re = re.compile(
                r'(([^\(\n]*?\)|\([^\)\n]*?)|([^\{\n]*?\}|\{[^\}\n]*?)|([^\[\n]*?\]|\[[^\]\n]*?))(\n|$)')
            self.partialquotes_re = re.compile(r'^((?:[^\"\n]*\"[^\"\n]*\")*[^\"\n]*)\"[^\"\n]*\n[^\"\n]*\"(\n|$)',
                                               flags=re.MULTILINE) # From StackOverflow
            self.partialquotes2_re = re.compile(r'^[^\"\n]*?\"(\n|$)', flags=re.MULTILINE)
            self.repeats_re = re.compile(r'(x|x )\d+')

        special_cases_removed = re.sub(self.specialcases_re, '', lyrics)
        nonlyric_tags_removed = re.sub(self.nonlyrictags_re, '', special_cases_removed)
        nonlyric_tags2_removed = re.sub(self.nonlyrictags2_re, '[', nonlyric_tags_removed)
        tags_removed = re.sub(self.tags_re, '', nonlyric_tags2_removed)
        chorus_verse_removed = re.sub(self.chorusverse_re, '', tags_removed)
        colons_removed = re.sub(self.colons_re, '\g<1>', chorus_verse_removed)
        quotes_removed = re.sub(self.quotes_re, '\n', colons_removed)  # Subing \n is to preserve the prior line
        asterisks_removed = re.sub(self.asterisks_re, '\n', quotes_removed)  # Seperate expression to not compete with the *scratching* filter
        partial_parens_removed = re.sub(self.partialparens_re, '', asterisks_removed)
        partial_quotes_removed = re.sub(self.partialquotes_re, '\g<1>\n', partial_parens_removed)
        partial_quotes2_removed = re.sub(self.partialquotes2_re, '', partial_quotes_removed)
        repeats_removed = re.sub(self.repeats_re, '', partial_quotes2_removed)
        return repeats_removed

    def _clean_characters(self, lyrics):
        if not hasattr(self, 'weirdchar_re'):
            self.weirdchar_re = re.compile(r'(~|\.{2,}|\+|\>|\<|\?(?=[^\n]))')  # Leave in -{2,} because of blurred out curse words
            self.endings_re = re.compile(r'(!|\?){2,}')  # Need to check ??? and !?!? cases
            self.endcommahyph_re = re.compile(r'(\b,|\-)( |\t)*?(\n|$)')

        weird_char_removed = re.sub(self.weirdchar_re, '', lyrics)
        endings_removed = re.sub(self.endings_re, '\g<1>', weird_char_removed)
        end_comma_hyph_removed = re.sub(self.endcommahyph_re, '\n', endings_removed)
        return end_comma_hyph_removed

    def _remove_single_words(self, lyrics):
        if not hasattr(self, 'onewordline_re'):
            self.onewordline_re = re.compile(r'^( |\t)*?\S+?( |\t)*?(\n|$)', flags=re.MULTILINE)

        one_word_line_removed = re.sub(self.onewordline_re, '', lyrics)
        return one_word_line_removed

    def _remove_whitespace(self, lyrics):
        if not hasattr(self, 'spaces_re'):
            self.spaces_re = re.compile(r'^( |\t)+?(\b|\')', flags=re.MULTILINE)
            self.endspaces_re = re.compile(r'( |\t)+?(\n|$)')
            self.midspaces_re = re.compile(r'( |\t){2,}')
            self.newline_re = re.compile(r'\n{2,}')
            self.beginninglines_re = re.compile(r'^\n{1,}')
            self.endinglines_re = re.compile(r'\n{1,}$')

        spaces_removed = re.sub(self.spaces_re, '\g<2>', lyrics)
        end_spaces_removed = re.sub(self.endspaces_re, '\n', spaces_removed)
        mid_spaces_removed = re.sub(self.midspaces_re, ' ', end_spaces_removed)
        newline_removed = re.sub(self.newline_re, '\n', mid_spaces_removed)
        beginning_lines_removed = re.sub(self.beginninglines_re, '', newline_removed)
        ending_lines_removed = re.sub(self.endinglines_re, '', beginning_lines_removed)
        return ending_lines_removed
