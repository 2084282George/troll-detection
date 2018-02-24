#!/bin/bash
for file1 in ./newSamples/*.txt; do
    [ -e "$file1" ] || continue
    for file2 in ./newSamples/*.txt; do
        [ -e "$file2" ] || continue
        $1 file1 file2 >> ./runs/FirstTest.csv
    done
done