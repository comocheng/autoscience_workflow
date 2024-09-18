#!/bin/bash

suffix=$(printf "%06.0f" $(($1)))
reaction_dir="$AUTOSCIENCE_REPO/dft/kinetics/reaction_$suffix"

if test -f "$reaction_dir/arkane/RMG_libraries/reactions.py" ; then
    echo "Arkane complete"
    exit 0
else
    echo "Arkane:"
    if test -d "$reaction_dir/arkane/" ; then
        ls
    fi
fi
echo

echo "Overall:"
if test -d "$reaction_dir/overall/" ; then
    cd "$reaction_dir/overall/"
    grep -l Normal *_*.log
fi
echo

echo "Center:"
if test -d "$reaction_dir/center/" ; then
    cd "$reaction_dir/center/"
    grep -l Normal *_*.log
fi
echo

echo "Shell:"
if test -d "$reaction_dir/shell/" ; then
    cd "$reaction_dir/shell/"
    grep -l Normal *_*.log
fi
echo

echo "HFSP:"
if test -d "$reaction_dir/hfsp/" ; then
    cd "$reaction_dir/hfsp/"
    grep -l Normal *_*.log
fi
echo
