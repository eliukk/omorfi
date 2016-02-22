#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Additional string handling functions for omorfi processing.

Includes some neat error logging for debugs and stuff."""

# Author: Tommi A Pirinen <flammie@iki.fi> 2015

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

from sys import stderr
import re
import unicodedata


def require_suffix(wordmap, suffix):
    if not wordmap['lemma'].endswith(suffix):
        fail_guess_because(wordmap, [], [suffix])


def remove_suffix(s, suffix):
    if s.endswith(suffix):
        return s[:s.rfind(suffix)]
    else:
        return s


def remove_suffixes_or_die(s, suffixes):
    for suffix in suffixes:
        nu = remove_suffix(s, suffix)
        if nu != s:
            return nu
    print("\033[91mUnstubbable!\033[0m Trying to rstrip ", ", ".join(suffixes),
          "from", s, file=stderr)
    return None


def replace_suffix(s, suffix, repl):
    if s.endswith(suffix):
        return s[:s.rfind(suffix)] + repl + s[s.rfind(suffix):]
    else:
        return s


def replace_suffixes_or_die(s, suffixes, repl):
    for suffix in suffixes:
        nu = replace_suffix(s, suffix, repl)
        if nu != s:
            return nu
    print("\033[91mSuffix fail!\033[0m Trying to rstrip ", ", ".join(suffixes),
          "from", s, file=stderr)
    return s


def mangle_suffixes_or_die(wordmap, suffixes):
    wordmap['bracketstub'] = replace_suffixes_or_die(wordmap['stub'], suffixes,
                                                     '<Del>→')
    wordmap['stub'] = remove_suffixes_or_die(wordmap['stub'], suffixes)
    if wordmap['stub'] == None:
        print("Word has been misclassified or suffix stripping is insufficient."
              "Fix the database or stripping rules to continue.",
              "Relevant word entry:\n", wordmap, file=stderr)
        exit(1)
    return wordmap


def replace_rightmost(s, needle, repl):
    '''Replace one occurrence of rightmost match.'''
    return replace_rightmosts(s, [needle], [repl])


def replace_rightmosts(s, needles, repls):
    '''Perform replacement on the rightmost matching substring from the list.
    '''
    rm = -1
    rmi = -1
    for i in range(len(needles)):
        pos = s.rfind(needles[i])
        if pos > rm:
            rm = pos
            rmi = i
    if rm != -1:
        s = s[:rm] + repls[rmi] + s[rm + len(needles[rmi]):]
    else:
        print("Suspicious replacement attempts!", file=stderr)
        print("tried to ", needles, " => ", repls, " in ", s, file=stderr)
    return s


def strip_diacritics(s):
    '''Convert Unicode characters with diacritics to their plain variants.'''
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

r_consonant = r'[kptgbdsfhvjlrmnczwxq]'
r_syllable = strip_diacritics(
    r_consonant + '*' + r'([aeiouyäö]|aa|ee|ii|oo|uu|yy|ää|öö|ai|ei|oi|ui|yi|äi|öi|au|eu|iu|ou|ey|iy|äy|öy|ie|uo|yö)' + r_consonant + '*')
re_two_syllable = re.compile(r'\b(' + r_syllable + r'){2}$')
re_three_syllable = re.compile(r'\b(' + r_syllable + r'){3}$')


def three_syllable(s):
    '''Return True if given word, or its last compound part, has unambiguously three syllables.'''
    s = strip_diacritics(s.lower())
    return(re_three_syllable.search(s) and not re_two_syllable.search(s))
