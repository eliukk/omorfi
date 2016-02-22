#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions to format FTB 3.1 style analyses from omorfi data."""

# Author: Omorfi contributors <omorfi-devel@groups.google.com> 2015

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# utils to format apertium style data from omorfi database values

from .formatter import Formatter
from .lexc_formatter import lexc_escape
from .settings import word_boundary, weak_boundary, \
    morph_boundary, deriv_boundary, optional_hyphen
from .error_logging import fail_formatting_missing_for, fail_guess_because, \
    just_fail


class Ftb3Formatter(Formatter):
    multichars = {
        '% A',
        '% V',
        '% N',
        '% Part',
        '% Abbr',
        '% Pron',
        '% Num',
        '% Prop',
        '% Interj',
        '% Dem',
        '% Interr',
        '% Rel',
        '% Qnt',
        '% Refl',
        '% N% Abbr',
        '% %>%>%>',
        '% CS',
        '% CC',
        '% Adv',
        '% Adp',
        '% Po',
        '% Pr',
        '% Adp% Po',
        '% Adp% Pr',
        '% Punct',
        '% Quote',
        '% EmDash',
        '% EnDash',
        '% Dash',
        '% Digit',
        '% Roman',
        '% Nom',
        '% Par',
        '% Gen',
        '% Ine',
        '% Ela',
        '% Ill',
        '% Ade',
        '% Abl',
        '% All',
        '% Ess',
        '% Ins',
        '% Abe',
        '% Tra',
        '% Com',
        '% Lat',
        '% Acc',
        '% Sg',
        '% Pl',
        '% PxSg1',
        '% PxSg2',
        '% PxPl1',
        '% PxPl2',
        '% PxPl3',
        '% Px3',
        '% TrunCo',
        'TrunCo% ',
        '% TruncPrefix',
        'TruncSuffix% ',
        '% Prt',
        '% Prs',
        '% Pst',
        '% Cond',
        '% Pot',
        '% Impv',
        '% Opt',
        '% Sg1',
        '% Sg2',
        '% Sg3',
        '% Pl1',
        '% Pl2',
        '% Pl3',
        '% Pe4',
        '% ConNeg',
        '% Neg',
        '% Act',
        '% Pass',
        '% Inf1',
        '% Inf2',
        '% Inf3',
        '% Inf5',
        '% PrsPrc',
        '% PrsPrc% Act',
        '% PrsPrc% Pass',
        '% PrfPrc',
        '% PrfPrc% Act',
        '% PrfPrc% Pass',
        '% AgPrc',
        '% NegPrc',
        '% Pos',
        '% Comp',
        '% Superl',
        "% Dem",
        "% Qnt",
        "% Pers",
        "% Indef",
        "% Interr",
        "% Refl",
        "% Rel",
        '% Ord',
        '% Foc%_hAn',
        '% Foc%_kAAn',
        '% Foc%_kin',
        '% Foc%_kO',
        '% Foc%_pA',
        '% Foc%_s',
        '% Foc%_kA',
        '% Man',
        '% Forgn',
        '%<Del%>→',
        '←%<Del%>'}

    stuff2ftb3 = {"Bc": "#",
                  ".sent": "",
                  ".": ".",
                  "Aa": "",
                  "Aan": "",
                  "ABBREVIATION": "% Abbr",
                  "ABESSIVE": "% Abe",
                  "ABLATIVE": "% Abl",
                  "ACRONYM": "% N% Abbr",
                  "ADESSIVE": "% Ade",
                  "ADJ": "% A",
                  "ADJECTIVE": "% A",
                  "ADP": "% Adp% Po",
                  "ADV": "% Adv",
                  "ADVERBIAL": "",
                  "Aen": "",
                  "Ahan": "",
                  "Ahen": "",
                  "Ahin": "",
                  "Ahon": "",
                  "Ahun": "",
                  "Ahyn": "",
                  "Ahän": "",
                  "Ahön": "",
                  "Aia": "",
                  "Aiden": "",
                  "Aien": "",
                  "Aihin": "",
                  "Aiin": "",
                  "Ain": "",
                  "Aisiin": "",
                  "Aita": "",
                  "Aitten": "",
                  "Aitä": "",
                  "Aiä": "",
                  "Aja": "",
                  "Ajen": "",
                  "Ajä": "",
                  "ALLATIVE": "% All",
                  "Ana": "",
                  "Aon": "",
                  "ARROW": "",
                  "Asa": "",
                  "Aseen": "",
                  "Ata": "",
                  "Aten": "",
                  "Atä": "",
                  "Aun": "",
                  "Ayn": "",
                  "Aä": "",
                  "Aän": "",
                  "Aön": "",
                  "B-": "% TrunCo",
                  "B←": "% TrunCo",
                  "B→": "TrunCo% ",
                  "CARDINAL": "",
                  "ORDINAL": "% Ord",
                  "Ccmp": "% Comp",
                  "CLAUSE-BOUNDARY": "",
                  "Cma": "% AgPrc",
                  "Cmaisilla": "% Adv",
                  "Cmaton": "% NegPrc",
                  "Cnut": "% PrfPrc",
                  "COMMA": "",
                  "COMPARATIVE": "",
                  "COMP": "% Comp",
                  "CONJ": "% CC",
                  "COORDINATING": "",
                  "Cpos": "% Pos",
                  "Csup": "% Superl",
                  "Cva": "% PrsPrc",
                  "DASH": "% Dash",
                  "DECIMAL": "",
                  "DEMONSTRATIVE": "% Dem",
                  "DERSTI": "",
                  "DERTTAIN": "",
                  "DIGIT": "% Digit",
                  "Din": "",
                  "Dinen": "",
                  "Dja": "",
                  "Dma": "% AgPrc",
                  "Dmaisilla": "% Inf5",
                  "Dmaton": "% NegPrc",
                  "Dminen": "% N",
                  "Dmpi": "",
                  "Dnut": "% PrfPrc% Act",
                  "Ds": "",
                  "Dsti": "",
                  "Dtattaa": "",
                  "Dtatuttaa": "",
                  "Dtava": "% PrsPrc% Pass",
                  "Dttaa": "",
                  "Dttain": "",
                  "Dtu": "% PrfPrc% Pass",
                  "Du": "",
                  "Duus": "",
                  "Dva": "% PrsPrc% Act",
                  "ELATIVE": "% Ela",
                  "FINAL-BRACKET": "",
                  "FINAL-QUOTE": "% Quote",
                  "FRACTION": "",
                  "FTB3man": "% Man",
                  "FTB3MAN": "% Man",
                  "GENITIVE": "% Gen",
                  "Ia": "% Inf1",
                  "Ie": "% Inf2",
                  "ILLATIVE": "% Ill",
                  "Ima": "% Inf3",
                  "Iminen": "% N",
                  "INDEFINITE": "% Indef",
                  "INESSIVE": "% Ine",
                  "INITIAL-BRACKET": "",
                  "INITIAL-QUOTE": "% Quote",
                  "INSTRUCTIVE": "% Man",
                  "INTERROGATIVE": "% Interr",
                  "INTJ": "% Interj",
                  "LATIVE": "% Lat",
                  "LEMMA-START": "",
                  "LOCATIVE": "% Ess",
                  "MULTIPLICATIVE": "",
                  "Ncon": "% ConNeg",
                  "Nneg": "% Neg",
                  "NOUN": "% N",
                  "Npl": "% Pl",
                  "N??": "% Sg",
                  "Nsg": "% Sg",
                  "NUMERAL": "% Num",
                  "NUM": "% Num",
                  "O3": "% Px3",
                  "Opl1": "% PxPl1",
                  "Opl2": "% PxPl2",
                  "Osg1": "% PxSg1",
                  "Osg2": "% PxSg2",
                  "PARTICLE": "% Part",
                  "PARTITIVE": "% Par",
                  "PE4": "% Pe4",
                  "PERSONAL": "% Pers",
                  "PL1": "% Pl1",
                  "PL2": "% Pl2",
                  "PL3": "% Pl3",
                  "Ppe4": "% Pe4",
                  "Ppl1": "% Pl1",
                  "Ppl2": "% Pl2",
                  "Ppl3": "% Pl3",
                  "PREPOSITION": "% Adp% Pr",
                  "PRONOUN": "% Pron",
                  "PRON": "% Pron",
                  "PROPER": "% Prop",
                  "Psg1": "% Sg1",
                  "Psg2": "% Sg2",
                  "Psg3": "% Sg3",
                  "PUNCTUATION": "% Punct",
                  "Qhan": "% Foc%_hAn",
                  "Qkaan": "% Foc%_kAAn",
                  "Qka": "% Foc%_kA",
                  "Qkin": "% Foc%_kin",
                  "Qko": "% Foc%_kO",
                  "Qpa": "% Foc%_pA",
                  "Qs": "% Foc%_s",
                  "QUALIFIER": "% A",
                  "QUANTIFIER": "% Qnt",
                  "QUANTOR": "% Qnt",
                  "RECIPROCAL": "",
                  "REFLEXIVE": "% Refl",
                  "RELATIVE": "% Rel",
                  "ROMAN": "% Roman",
                  "SCONJ": "% CS",
                  "SENTENCE-BOUNDARY": "",
                  "SEPARATIVE": "% Par",
                  "SG1": "% Sg1",
                  "SG2": "% Sg2",
                  "SG3": "% Sg3",
                  "SPACE": "",
                  "SUFFIX": "",
                  "SUPERL": "% Superl",
                  "Tcond": "% Cond",
                  "Timp": "% Impv",
                  "Topt": "% Opt",
                  "Tpast": "% Pst",
                  "Tpot": "% Pot",
                  "Tpres": "% Prs",
                  "Uarch": "",
                  "Udial": "",
                  "Unonstd": "",
                  "UNSPECIFIED": "% Adv",
                  "Urare": "",
                  "Vact": "% Act",
                  "VERB": "% V",
                  "Vpss": "% Pass",
                  "X": "",
                  "Xabe": "% Abe",
                  "Xabl": "% Abl",
                  "Xacc": "% Acc",
                  "Xade": "% Ade",
                  "Xall": "% All",
                  "Xcom": "% Com",
                  "Xela": "% Ela",
                  "Xess": "% Ess",
                  "XForeign": "% Forgn",
                  "Xgen": "% Gen",
                  "Xill": "% Ill",
                  "Xine": "% Ine",
                  "Xins": "% Ins",
                  "Xlat": "% Lat",
                  "X???": "% Nom",
                  "Xnom": "% Nom",
                  "Xpar": "% Par",
                  "Xtra": "% Tra",
                  "": ""
                  }

    def __init__(this, verbose=True):
        this.verbose = verbose
        fail = False
        for stuff, ftb3 in this.stuff2ftb3.items():
            if len(ftb3) < 2:
                continue
            elif not ftb3 in this.multichars:
                just_fail("There are conflicting formattings in here!\n" +
                          ftb3 + " for " + stuff +
                          " is not a valid defined ftb3 multichar_symbol!")
                fail = True
        if fail:
            this.tainted = True

    def stuff2lexc(this, stuff):
        if stuff == '0':
            return "0"
        elif stuff in this.stuff2ftb3:
            return this.stuff2ftb3[stuff]
        else:
            if this.verbose:
                fail_formatting_missing_for(stuff, "ftb3.1")
            return ""

    def analyses2lexc(this, anals):
        ftbstring = ""
        if 'Nneg|Vact' in anals:
            anals = anals.replace('|Vact', '')
        elif anals == 'Vact|Ia|Xlat':
            anals = 'Ia|Xlat'
        elif anals == 'Vact|Ima|Xins':
            anals = 'Ima|FTB3man'
        elif 'Vact|Ima' in anals:
            anals = anals.replace('Vact|', '')
        elif anals == 'Vact|Ie|Nsg|Xins':
            anals = 'Ie|Vact|FTB3man'
        elif anals == 'Vact|Tpres|Ppe4|Ncon':
            anals = 'Vact|Tpres|Ncon'
        elif anals == 'Vpss|Tpres|Ppe4|Ncon':
            anals = 'Vpss|Tpres|Ncon'
        elif 'Dmaton' in anals:
            anals = anals.replace('Dmaton', 'Cmaton')
        elif 'Dma' in anals:
            anals = anals.replace('Dma', 'Cma')
        parts = anals.split('|')
        # Here is a bit of puzzle
        # I < X
        # V < X
        # T < V
        # C < V
        # X < S
        # -----
        # I < T,C < V < X < N
        reordered = []
        # append I first
        for part in parts:
            if part.startswith('I'):
                # Infinitive I before case X
                reordered.append(part)
        # then T or C
        for part in parts:
            if part.startswith('T'):
                # Tense T before Voice V
                reordered.append(part)
            elif part.startswith('C'):
                # Participle C before voice V
                reordered.append(part)
        # then V
        for part in parts:
            if part.startswith('V'):
                # Voice V before Case X
                reordered.append(part)
        # then X
        for part in parts:
            if part.startswith('X'):
                # Case X before Number N
                reordered.append(part)
        # then rest in their natural order
        parts = [x for x in parts
                 if not x.startswith('X') and not x.startswith('T')
                 and not x.startswith('C') and not x.startswith('I')
                 and not x.startswith('V')]
        for part in parts:
            reordered.append(part)
        for anal in reordered:
            ftbstring += this.stuff2lexc(anal)
        return ftbstring

    def continuation2lexc(this, anals, surf, cont):
        ftbstring = this.analyses2lexc(anals)
        if 'COMPOUND' in cont:
            # XXX: there was += before
            ftbstring = surf.replace(
                morph_boundary, '').replace(deriv_boundary, '')
        elif 'NUM_' in cont and ('BACK' in cont or 'FRONT' in cont and not ('CLIT' in cont or 'POSS' in cont)):
            ftbstring += surf.replace(morph_boundary,
                                      '').replace(deriv_boundary, '')
        elif 'DIGITS_' in cont and not ('BACK' in cont or 'FRONT' in cont):
            ftbstring = lexc_escape(surf) + ftbstring
        surf = lexc_escape(surf)
        return "%s:%s\t%s ;\n" % (ftbstring, surf, cont)

    def wordmap2lexc(this, wordmap):
        '''
        format string for canonical ftb3 format for morphological analysis
        '''
        if wordmap['stub'] == ' ':
            # do not include normal white space for now
            return ""
        wordmap['stub'] = lexc_escape(
            wordmap['stub'].replace(word_boundary, optional_hyphen))
        wordmap['analysis'] = "%s" % (
            lexc_escape(wordmap['bracketstub'].replace(word_boundary, '#') + '←<Del>'))
        if (wordmap['pos'] == 'ACRONYM' and (len(wordmap['stub']) == 1 and
                                             not wordmap['stub'].isalpha())) or wordmap['stub'] == '§§':
            wordmap['analysis'] += this.stuff2lexc('PUNCTUATION')
        elif wordmap['pos'] in ['NOUN', 'VERB', 'ADJECTIVE', 'PRONOUN',
                                'NUMERAL', 'ACRONYM', 'PUNCTUATION', 'SUFFIX']:
            wordmap['analysis'] += this.stuff2lexc(wordmap['pos'])
        elif wordmap['pos'] == 'CONJUNCTIONVERB':
            if wordmap['lemma'] == 'eikä':
                wordmap['analysis'] = wordmap['lemma'] + this.stuff2lexc('CONJ') + \
                    this.stuff2lexc('Nneg')
            else:
                wordmap['analysis'] += this.stuff2lexc('ADVERBIAL') + \
                    this.stuff2lexc('Nneg')
        elif wordmap['pos'] == 'PARTICLE':
            if wordmap['upos'] in ['CONJ', 'SCONJ', 'INTJ', 'ADV', 'ADP']:
                wordmap['analysis'] += this.stuff2lexc(wordmap['upos'])
            else:
                wordmap['analysis'] += this.stuff2lexc('PARTICLE')
        elif wordmap['pos'] == 'PROPN':
            print("???", wordmap)
        elif wordmap['pos'] == 'X':
            # FORGN etc.
            wordmap['analysis'] += this.stuff2lexc('NOUN')
        else:
            fail_guess_because(wordmap, [], ["PARTICLE", "PROPN",
                                             'NOUN', 'VERB', 'ADJECTIVE', 'PRONOUN', 'NUMERAL',
                                             'ACRONYM', 'PUNCTUATION'],
                               "not in FTB3 known poses or particle!")
            exit(1)
        if wordmap['prontype']:
            if 'PERSONAL' in wordmap['prontype']:
                wordmap['prontype'] = 'PERSONAL'
            for stuff in wordmap['prontype'].split("|"):
                wordmap['analysis'] += this.stuff2lexc(stuff)
        if wordmap['lex']:
            for stuff in wordmap['lex'].split("|"):
                wordmap['analysis'] += this.stuff2lexc(stuff)
        if wordmap['abbr']:
            for stuff in wordmap['abbr'].split("|"):
                wordmap['analysis'] += this.stuff2lexc(stuff)
        if wordmap['numtype']:
            for stuff in wordmap['numtype'].split("|"):
                wordmap['analysis'] += this.stuff2lexc(stuff)
        if wordmap['is_proper']:
            wordmap['analysis'] += this.stuff2lexc('PROPER')
        if wordmap['symbol']:
            for subcat in wordmap['symbol'].split('|'):
                wordmap['analysis'] += this.stuff2lexc(subcat)
            if wordmap['lemma'] == '–':
                wordmap['analysis'].replace('Dash', 'EnDash')
            if wordmap['lemma'] == '—':
                wordmap['analysis'].replace('Dash', 'EmDash')
        lex_stub = wordmap['stub']
        retvals = []
        retvals += ["%s:%s\t%s\t;" % (wordmap['analysis'], lex_stub,
                                      wordmap['new_para'])]
        if wordmap['lemma'] in ['-', '–', '—', '(']:
            retvals += ["%s%% %%>%%>%%>:%s\t%s\t;" % (wordmap['analysis'], lex_stub,
                                                      wordmap['new_para'])]
        return "\n".join(retvals)

    def multichars_lexc(this):
        multichars = "Multichar_Symbols\n"
        multichars += "!! FTB 3.1 multichar set:\n"
        for mcs in this.multichars:
            multichars += mcs + "\n"
        multichars += Formatter.multichars_lexc(this)
        return multichars

    def root_lexicon_lexc(this):
        root = Formatter.root_lexicon_lexc(this)
        if True:
            # want co-ordinated hyphens left
            root += "!! LEXICONS that can be co-ordinated hyphen -compounds\n"
            root += this.stuff2lexc('B→') + ':-   NOUN ;\n'
            root += this.stuff2lexc('B→') + ':-   ADJ ;\n'
            root += this.stuff2lexc('B→') + ':-   SUFFIX ;\n'
        return root

# self test
if __name__ == '__main__':
    formatter = Ftb3Formatter()
    exit(0)
