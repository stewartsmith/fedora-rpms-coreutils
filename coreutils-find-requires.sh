#!/bin/sh -
# Reduce requires for coreutils-single
# Needed since it has overlapping "binaries" with the main package
# Ideally we could do the following in the spec only for the single subpackage
# %define __requires_exclude_from ^(%{_bindir}|%{_sbindir})/([^c]|c[^o]|co[^r]|cor[^e])

original_find_requires="$1"
shift

# Get the list of files.
files=`sed "s/['\"]/\\\&/g"`

single_bin='/usr/bin/coreutils'

single=`echo $files | grep "$single_bin"`

echo $files | tr [:blank:] '\n' |
if [ "$single" ]; then
    # Only allow the coreutils multicall binary
    # Also adjust for .single renaming
    sed -n 's|\(.*'"$single_bin"'\)\(.single\)\?$|\1.single|p'
else
    cat
fi |
$original_find_requires
