#!/bin/bash
# This script takes a Finnish wiktionary xml dump and converts it to omorfi
# Originally from end assignment of CLT 131 in Uni. Helsinki by ...
# Bit of coding style fixes and updates by <flammie@iki.fi>

print_usage() {
    echo "Usage: $0 [fiwikt-pages-articles.xml]"
    echo
    echo "fiwikt-pages-articles.xml must point to unzipped fi.wiktionary dump."
    echo "If omitted, stdin is used"
}

if test $# -ge 2 ; then
    print_usage
    exit 1
fi

# Define word class
wc='(Substantiivi|Adjektiivi|Pronomini|Numeraali|Prepositio|Adverbi|Interjektio|Konjunktio|Partikkeli|Verbi|Erisnimi)'
# Fetch only relevant lines from the xml dump (NOTE: This assumes relevant 
# lines are between <page> & </page> tags)
cat $@ | sed -ne '/<page>/,/<\/page>/p' |\
# Remove all line-initial whitespaces
    sed -e 's/^[ \t]*//g' |\
# Remove unwanted xml tags
    sed -ne '/\(<page>\|<title>\)/p' -ne '/<text/,/<\/page>/p' |\
# Remove unwanted xml tag (NOTE: The </revision> tag is found between </text> 
# & </page>)
    sed '/<\/revision>/d' |\
# Remove linebreaks 
    tr -d '\n' |\
# Place linebreak infront of each <page>
    sed -re "s/<page>/\n\0/g" |\
# Retain only those lines which contain relevant content (in this case ==Suomi== which is the heading of Finnish words)
    fgrep "==Suomi==" |\
# Remove certain MediaWiki pages
    sed -r "/<title>(Luokka:)|(Malline:)|(Wikisanakirja:)/d" |\
# Place tags and content on separate lines
    sed -re "s/(<\/page>)/\n\1/g" \
    -e "s/(<title>)/\n\1/g" \
    -e "s/(<\/title>)/\1\n/g" \
    -e "s/(<text [^>]*>)/\1\n/g" \
    -e "s/(<\/text>)/\n\1/g" |\
# Place relevant content markup characters on seperate lines
    sed -re "s/(==*[[:alpha:]]+==)/\n\1/g" \
    -e "s/((\(\{\{)|(\{\{fi))/\n\1/g" \
    -e "s/(#)/\n\1/g" |\
# Parse lines and tag word classes in headings (example: ===Substantiivi===)
    sed -re "s/=$wc=/<wordclass>\1<\/wordclass>/g" |\
# Parse lines and tag with KOTUS numbering (this script only allows
# {{taivutustyyppi|99(alt: 99-A), {{fi-taivitus|99 & {{fi-subs-99 formats)
    sed -re "s/\{\{taivutustyyppi\|([[:alnum:]]+-?[[:alnum:]]?)\}\}/<kotus>\1<\/kotus>/" \
    -e "s/\{\{fi-taivutus\|([[:digit:]]+(\|?[[:upper:]])*)/<kotus>\1<\/kotus>/" \
    -e "s/\{\{fi-[[:alpha:]]*-([[:digit:]]+)\}\}/<kotus>\1<\/kotus>/" |\
# Parse lines that begin with # but not #: and tag with definition
    sed -re "s/^(#[^#:].*)$/<definition>\1<\/definition>/g" |\
# Parse lines that begin with #: and tag with example
    sed -re "s/^(#:.*)$/<example>\1<\/example>/g" |\
# Place tags on separate lines
    sed -re "s/(<(wordclass|kotus|definition|example)>.*<\/(wordclass|kotus|definition|example)>)/\n\1\n/g" |\
# Remove all  non-tagged lines
    sed -rn "/^<.*>$/p" |\
# Remove definitions that are for conjugated words, i.e. retain only
# definitions of unconjugated words
    sed -r "/(\{\{taivm)|(-taivm\|)|(\(taivutusmuoto)|(\(taivutusmuodot)|(taivutusmuoto'')|(\(taivus)/d" | egrep -v "\[\[Luokka:Suomen ([[:alpha:]]+) taivutusmuodot\]\]" |\
# Parse remove wikimedia links, formatting and other tuff
    sed -r "s/\[\[[[:alpha:]]+\|([[:alpha:]]+)\]\]/\1/g" |\
# Parse and remove other wikimedia markup "garbage"
    sed -re "/\[\[[[:alpha:]]+:[[:alpha:]]+.*\]\]/d" -e "/\{.*\}/d" | sed -re "s/\[|\]//g" -e "s/'|#|#://g" |\
# Remove unescessary <text> & </text> tags
    sed -re "/^<text |<\/text>/d" |\
# Rename remaining wiktionary xml tags: page to entry, title to lemma
    sed -re "s/page>$/entry>/g" -e "s/title>/lemma>/g" |
# Remove linebreaks
    tr -d '\n' |\
# Place each <entry> on a separate line
    sed -re "s/(<entry>)/\n\1/g" |\
# Place entries in alphabetical order (due to uniform xml strucuture sort
# command works normally) and write as .xml file
    sort |\
# pick all classified for now
    fgrep '<kotus' |\
# make csv
    sed -re 's/^.*<lemma>([^<]*).*<wordclass>([^<]*).*<kotus>([^<]*).*$/\1,\3,\2/' |\
# remove missing lemmas or classes shown as leftover tags from ^^
    fgrep -v '<entry>' |\
    tr '|' ',' |\
    sed -re 's/([[:digit:]]+)-([[:upper:]])/\1,\2/' |\
    gawk -F , 'NF == 3 {printf("\"%s\",\"%s\",\"0\",\"%s\"\n", $1, $2, $3);} NF == 4 {printf("\"%s\",\"%s\",\"%s\",\"%s\"\n", $1, $2, $3, $4);}' |\
    sed -e 's/Substantiivi/N/' -e 's/Adjektiivi/A/' -e 's/Numeraali/Num/' \
        -e 's/Verbi/V/' -e 's/Erisnimi/Prop/' -e 's/Pronomini/Pron/' \
        -e 's/Adverbi/Adv/' 
