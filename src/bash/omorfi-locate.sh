#!/bin/bash
omorfidir="/usr/local/share/omorfi"
homeomorfidir="$HOME/.omorfi"
localomorfidir0=.
localomorfidir1=generated
localomorfidir2=src/generated
localomorfidir3=../src/generated
function find_omorfi() {
    for d in $omorfidir $homeomorfidir $localomorfidir0 $localomorfidir1 \
        $localomorfidir2 $localomorfidir3 ; do
        if test $# = 0 ; then
            if test -d "$d" ; then
                echo "$d"
                break
            fi
        elif test $# = 1 ; then
            func=$1
            case $func in
            analyse|generate)
                for tagset in omor ftb3 ftb1 ; do
                    if test -f "$d/omorfi-$tagset.$func.hfst" ; then
                        echo "$d/omorfi-$tagset.$func.hfst"
                        break 2
                    fi
                done;;
            *)
                if test -f "$d/omorfi.$func.hfst" ; then
                    echo "$d/omorfi.$func.hfst"
                    break
                fi;;
            esac
        elif test $# = 2 ; then
            func=$1
            tagset=$2
            if test -f "$d/omorfi-$tagset.$func.hfst" ; then
                echo "$d/omorfi-$tagset.$func.hfst"
                break
            fi
        fi
    done
}

function find_help() {
    echo "Omorfi could not be located. Search path is:"
    for d in $omorfidir $homeomorfidir $localomorfidir0 $localomorfidir1 \
        $localomorfidir2 $localomorfidir3 ; do
        if test $# = 0 ; then
            echo $d
        elif test $# = 1 ; then
            func=$1
            case $func in
            analyse|generate)
                for tagset in omor ftb3 ftb1 ; do
                    echo "$d/omorfi-$tagset.$func.hfst"
                done;;
            *)
                echo "$d/omorfi.$func.hfst"
            esac
        elif test $# = 2 ; then
            func=$1
            tagset=$2
            echo "$d/omorfi-$tagset.$func.hfst"
        fi
    done

}
