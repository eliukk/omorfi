#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions to format giellatekno style analyses from omorfi data."""

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

from .lexc_formatter import lexc_escape
from .settings import word_boundary, weak_boundary, \
        morph_boundary, deriv_boundary, optional_hyphen
from .error_logging import fail_formatting_missing_for


giella_multichars= {
        '%+A',
        '%+V',
        '%+N',
        '%+Num',
        '%+Adv',
        '%+Pron',
        '%+Pcle',
        '%+Interj',
        '%+Abbr',
        '%+Num',
        '%+Prop',
        '%+Dem',
        '%+Interr',
        '%+Rel',
        '%+Qu',
        '%+Refl',
        '%+Pers',
        '%+N%+Abbr',
        '%+CS',
        '%+CC',
        '%+Adp',
        '%+Po',
        '%+Pr',
        '%+Adp%+Po',
        '%+Adp%+Pr',
        '%+Punct',
        '%+Quote',
        '%+Dash',
        '%+Digit',
        '%+Roman',
        '%+Card',
        '%+Ord',
        '%+Pref',
        '%+Suff',
        '%+Nom',
        '%+Par',
        '%+Gen',
        '%+Ine',
        '%+Ela',
        '%+Ill',
        '%+Ade',
        '%+Abl',
        '%+All',
        '%+Ess',
        '%+Ins',
        '%+Abe',
        '%+Tra',
        '%+Com' ,
        '%+Lat',
        '%+Acc',
        '%+Sg',
        '%+Pl',
        '%+PxSg1',
        '%+PxSg2',
        '%+PxSg3',
        '%+PxPl1',
        '%+PxPl2',
        '%+PxPl3',
        '%+TruncPrefix',
        'TruncSuffix%+',
        '%+Prt',
        '%+Prs',
        '%+Pst',
        '%+Cond',
        '%+Pot',
        '%+Impv',
        '%+Opt',
        '%+Sg1',
        '%+Sg2',
        '%+Sg3',
        '%+Pl1',
        '%+Pl2',
        '%+Pl3',
        '%+Pe4',
        '%+ConNeg' ,
        '%+Neg',
        '%+Act',
        '%+Pass',
        '%+InfA',
        '%+InfE',
        '%+InfMA',
        '%+Der/minen',
        '%+Der/maisilla',
        '%+PrsPrc',
        '%+PrsPrc%+Act',
        '%+PrsPrc%+Pass',
        '%+PrfPrc',
        '%+PrfPrc%+Act',
        '%+PrfPrc%+Pass',
        '%+AgPrc',
        '%+NegPrc',
        '%+Pos',
        '%+Comp',
        '%+Superl',
        "%+Dem",
        "%+Qnt",
        "%+Pers",
        "%+Indef",
        "%+Interr",
        "%+Refl",
        "%+Rel",
        '%+Ord',
        '%+Foc%/han',
        '%+Foc%/kaan',
        '%+Foc%/kin',
        '%+Qst',
        '%+Foc%/pa',
        '%+Foc%/s',
        '%+Foc%/ka',
        '%+Der%/sti',
        '%+Der%/ja',
        '%+Der%/inen',
        '%+Der%/lainen',
        '%+Der%/tar',
        '%+Der%/llinen',
        '%+Der%/ton',
        '%+Der%/tse',
        '%+Der%/vs',
        '%+Der%/u',
        '%+Der%/ttain',
        '%+Der%/ttaa',
        '%+Der%/tattaa',
        '%+Der%/tatuttaa',
        '%+Der%/uus',
        '%+Der%/nti',
        "%+Der%/sti",
        '%+Err%/Sub',
        '%+Use%/Marg',
        '%+Use%/Rare',
        '%+Use%/Circ',
        '%+Dial',
        '%+Dial%/Standard',
        '%+Dial%/East',
        '%+Dial%/West',
        '%+Dial%/Southwest',
        '%+Dial%/Häme',
        '%+Dial%/Eteläpohjalaiset',
        '%+Dial%/Keskipohjalaiset',
        '%+Dial%/Peräpohjalaiset',
        '%+Dial%/North',
        '%+Dial%/Savo',
        '%+Dial%/Southeast',
        '%+Sem%/Geo',
        '%+Sem%/Human',
        '%+Sem%/Org'}


stuff2giella = {"Bc": "#",
        ".sent": "",
        "B-": "%+Trunc",
        "B→": "TruncSuffix%+",
        "B←": "%+TruncPrefix",
        "Cma": "%+AgPrc",
        "Cmaisilla": "%+Der/maisilla",
        "Cnut": "%+PrfPrc",
        "Cva": "%+PrsPrc",
        "Cmaton": "%+NegPrc",
        "Cpos": "%+Pos",
        "Ccmp": "%+Comp",
        "Csup": "%+Superl",
        "Dmaisilla": "%+Der/maisilla",
        "Dminen": "%+N",
        "Dnut": "%+PrfPrc%+Act",
        "Dtu": "%+PrfPrc%+Pass",
        "Dva": "%+PrsPrc%+Act",
        "Dtava": "%+PrsPrc%+Pass",
        "Dmaton": "%+NegPrc",
        "Duus": "%+Der/uus",
        "Dttaa": "%+Der/ttaa",
        "Dtattaa": "%+Der/tattaa",
        "Dtatuttaa": "%+Der/tatuttaa",
        "Dma": "%+AgPrc",
        "Dinen": "%+Der/inint",
        "Dja": "%+Der/ja",
        "Dmpi": "%+Comp",
        "Din": "%+Superl",
        "Ds": "%+Cmp",
        "Du": "%+Der/u",
        "Dsti": "%+Der/sti",
        "FTB3man": "%+Man",
        "Ia": "%+Inf1",
        "Ie": "%+Inf2",
        "Ima": "%+Inf3",
        "Iminen": "%+N",
        "Ncon": "%+ConNeg",
        "Nneg": "%+Neg", 
        "Npl": "%+Pl", 
        "Nsg": "%+Sg", 
        "N??": "%+Sg",
        "Osg1": "%+PxSg1",
        "Osg2": "%+PxSg2",
        "O3": "%+Px3",
        "Opl1": "%+PxPl1",
        "Opl2": "%+PxPl2",
        "Ppl1": "%+Pl1", 
        "Ppl2": "%+Pl2",
        "Ppl3": "%+Pl3",
        "Psg1": "%+Sg1", 
        "Psg2": "%+Sg2",
        "Psg3": "%+Sg3",
        "Ppe4": "%+Pe4", 
        "Qka": "%+Foc%_kA",
        "Qs": "%+Foc%_s",
        "Qpa": "%+Foc%_pA",
        "Qko": "%+Foc%_kO",
        "Qkin": "%+Foc%_kin",
        "Qkaan": "%+Foc%_kAAn",
        "Qhan": "%+Foc%_hAn",
        "Tcond": "%+Cond",
        "Timp": "%+Impv", 
        "Tpast": "%+Pst",
        "Tpot": "%+Pot", 
        "Tpres": "%+Prs",
        "Topt": "%+Opt",
        "Uarch": "",
        "Udial": "%+Dial", 
        "Urare": "%+Use/Marg",
        "Unonstd": "%+Err/Orth",
        "Vact": "%+Act",
        "Vpss": "%+Pass",
        "Xabe": "%+Abe",
        "Xabl": "%+Abl",
        "Xade": "%+Ade",
        "Xall": "%+All",
        "Xcom": "%+Com",
        "Xela": "%+Ela",
        "Xess": "%+Ess", 
        "Xgen": "%+Gen",
        "Xill": "%+Ill", 
        "Xine": "%+Ine",
        "Xins": "%+Ins",
        "Xnom": "%+Nom",
        "Xpar": "%+Par", 
        "Xtra": "%+Tra", 
        "Xlat": "%+Lat",
        "Xacc": "%+Acc",
        "X???": "%+Nom",
        "NOUN": "%+N",
        "ADJECTIVE": "%+A", 
        "QUALIFIER": "%+A",
        "VERB": "%+V",
        "ADVERB": "%+Adv",
        "INTERJECTION": "%+Interj",
        "PRONOUN": "%+Pron",
        "NUMERAL": "%+Num",
        "ADPOSITION": "%+Adp%+Po",
        "PREPOSITION": "%+Adp%+Pr",
        "CONJUNCTION": "",
        "COORDINATING": "%+CC",
        "ADVERBIAL": "%+CS",
        "COMPARATIVE": "%+CS",
        "ABBREVIATION": "%+ABBR",
        "ACRONYM": "%+ACR",
        "PROPER": "%+Prop",
        "CARDINAL": "",
        "ORDINAL": "%+Ord",
        "DEMONSTRATIVE": "%+Dem",
        "QUANTOR": "%+Qnt",
        "PERSONAL": "%+Pers",
        "INDEFINITE": "%+Indef",
        "INTERROGATIVE": "%+Interr",
        "REFLEXIVE": "%+Refl",
        "RELATIVE": "%+Rel",
        "RECIPROCAL": "",
        "PUNCTUATION": "%+Punct",
        "DASH": "%+Dash",
        "SPACE": "",
        "DECIMAL": "",
        "CLAUSE-BOUNDARY": "",
        "SENTENCE-BOUNDARY": "",
        "INITIAL-QUOTE": "%+Quote",
        "FINAL-QUOTE": "%+Quote",
        "INITIAL-BRACKET": "",
        "FINAL-BRACKET": "",
        "COMMA": "",
        "ARROW": "",
        "DIGIT": "%+Digit",
        "ROMAN": "%+Roman",
        "PL1": "%+Pl1", 
        "PL2": "%+Pl2",
        "PL3": "%+Pl3",
        "SG1": "%+Sg1", 
        "SG2": "%+Sg2",
        "SG3": "%+Sg3",
        "PE4": "%+Pe4",
        "COMP": "%+Comp",
        "SUPERL": "%+Superl",
        "UNSPECIFIED": "%+Pcle",
        "DERSTI": "%+Der%/sti",
        "DERTTAIN": "%+Der%/ttain",
        "INESSIVE": "%+Ine",
        "ILLATIVE": "%+Ill",
        "ADESSIVE": "%+Ade",
        "ALLATIVE": "%+All",
        "ABLATIVE": "%+Abl",
        "LOCATIVE": "",
        "FTB3MAN": "%+Ins",
        "PARTICLE": "%+Pcle",
        "LEMMA-START": "",
        "GEO": "%+Sem%/Geo",
        "FIRST": "%+Sem%/Human",
        "LAST": "%+Sem%/Human",
        "ORG": "%+Sem%/Org",
        "CULTGRP": "%+Sem/Human",
        "PRODUCT": "",
        "MISC": "",
        "MEDIA": "",
        "ARTWORK": "",
        "EVENT": "",
        ".":"",
        "": ""
        }

def format_stuff_giella(stuff):
    if stuff == '0':
        return "0"
    elif stuff in stuff2giella:
        return stuff2giella[stuff]
    else:
        fail_formatting_missing_for(stuff, "giella.1")
        return ""

def format_analysis_lexc_giella(anals):
    ftbstring = ""
    for anal in anals.split('|'):
        ftbstring += format_stuff_giella(anal)
    return ftbstring

def format_continuation_lexc_giella(anals, surf, cont):
    ftbstring = format_analysis_lexc_giella(anals)
    if 'DIGITS_' in cont and not ('BACK' in cont or 'FRONT' in cont):
        ftbstring = lexc_escape(surf) + ftbstring
    surf = lexc_escape(surf)
    return "%s:%s\t%s ;\n" %(ftbstring, surf, cont)

def format_wordmap_lexc_giella(wordmap):
    '''
    format string for canonical giella format for morphological analysis
    '''
    wordmap['analysis'] = lexc_escape(wordmap['lemma'].replace(word_boundary, '#'))
    if wordmap['pos'] == 'CONJUNCTIONVERB':
        if wordmap['lemma'] == 'eikä':
            wordmap['lemma'] = 'ei'
            wordmap['analysis'] = format_stuff_giella('COORDINATING') + \
                    format_stuff_giella('Nneg')
        else:
            wordmap['analysis'] = format_stuff_giella('ADVERBIAL') + \
                    format_stuff_giella('Nneg')
    else:
        wordmap['analysis'] += format_stuff_giella(wordmap['pos'])
    if wordmap['is_proper']:
        wordmap['analysis'] += format_stuff_giella('PROPER')
        if wordmap['proper_noun_class']:
            wordmap['analysis'] += format_stuff_giella(wordmap['proper_noun_class'])
    if wordmap['particle']:
        for pclass in wordmap['particle'].split('|'):
            wordmap['analysis'] += format_stuff_giella(pclass)
    if wordmap['symbol']:
        for subcat in wordmap['symbol'].split('|'):
            wordmap['analysis'] += format_stuff_giella(subcat)
    lex_stub = lexc_escape(wordmap['stub'].replace(word_boundary, "#").replace(weak_boundary, "").replace(deriv_boundary, "»"))
    retvals = []
    retvals += ["%s:%s\t%s\t;" %(wordmap['analysis'], lex_stub, 
                wordmap['new_para'])]
    return "\n".join(retvals)

def format_multichars_lexc_giella():
    multichars = "!! giellatekno multichar set:\n"
    for mcs in giella_multichars:
        multichars += mcs + "\n"
    return multichars

# self test
if __name__ == '__main__':
    fail = False
    for stuff, giella in stuff2giella.items():
        if len(giella) < 2:
            continue
        elif not giella in giella_multichars:
            print("There are conflicting formattings in here!", giella, 
                    "is not a valid defined giella multichar_symbol!")
            fail = True
    if fail:
        exit(1)

