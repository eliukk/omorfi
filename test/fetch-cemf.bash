#!/bin/bash
curl "http://kaino.kotus.fi/korpus/1800/meta/1800_coll_rdf.xml" | grep -a '"/korpus/1800/teksti/' | sed 's|.*"/korpus/1800/meta/\(.*\)".*|http://kaino.kotus.fi/korpus/1800/meta/\1|' | xargs wget --continue -P cemf-list
grep -h -a kotus:class cemf-list/*.xml | sed 's|.*rdf:resource="\(.*\)" kotus:class.*|\1|' | sed 's|^|http://kaino.kotus.fi|' | xargs wget --continue -P cemf
rm -rf cemf-list
mkdir cemf-dict
mv cemf/calamnius_aristoteleen_runousoppi1871.xml cemf-dict
mv cemf/forkortningar1865.xml cemf-dict
mv cemf/forord1853.xml cemf-dict
mv cemf/forord1865.xml cemf-dict
mv cemf/forordforklaringar1853.xml cemf-dict
mv cemf/helenius.xml cemf-dict
mv cemf/kilpinen_medictermin1844.xml cemf-dict
mv cemf/lexik1865.xml cemf-dict
mv cemf/renvall.xml cemf-dict
mv cemf/sanakirja1853.xml cemf-dict
mv cemf/sanakirja1883-1890.xml cemf-dict
mv cemf/socknenamn1853.xml cemf-dict
mv cemf/ticklen_terminimedici1832.xml cemf-dict
mv cemf/hoijerin_soitanto1877.xml cemf-dict
