#!/bin/bash
source $(dirname $0)/omorfi.bash
args=$@

function print_version() {
    echo "omorfi-analyse-text 0.3 (Using omorfi bash API ${omorfiapi})"
    echo "Copyright (c) 2016 Tommi A Pirinen"
    echo "Licence GPLv3: GNU GPL version 3 <http://gnu.org/licenses/gpl.html>"
    echo "This is free software: you are free to change and redistribute it."
    echo "There is NO WARRANTY, to the extent permitted by law."

}

function print_usage() {
    echo "Usage: $0 [OPTION] [FILENAME...]"
}

function print_help() {
    echo "Analyses running text using omorfi automata and hfst tools"
    echo
    echo "  -h, --help      Print this help dialog"
    echo "  -V, --version   Print version info"
    echo "  -v, --verbose   Print verbosely while processing"
    echo "  --tagset TAGS   Use TAGS analyser"
    echo
    echo "If no FILENAMEs are given, input is read from standard input."
    echo "This program uses hfst-apertium-proc and, if found"
    echo "apertium-destxt, otherwise sed"
}

if test x$1 == x-h -o x$1 == x--help ; then
    print_usage
    print_help
    exit 0
elif test x$1 == x-V -o x$1 == x--version ; then
    print_version
    exit 0
elif test x$1 == x-v -o x$1 == x--verbose ; then
    verbose=verbose
    shift 1
elif test x$1 == x--tagset ; then 
    tagset=$2
    shift 2
fi
if test -z "$tagset" ; then
    tagset=omor
fi
if test x$verbose = xverbose ; then
    echo "Trying to use $tagset to analyse... $@"
    if test $# -eq 0 ; then
        echo "Reading from <stdin>"
        echo "THIS TOOL DOES NOT PRINT OUTPUT IMMEDIATELY AT LINEBREAK/ENTER"
    fi
fi
cat $@ | omorfi_analyse_text $tagset
