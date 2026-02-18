#!/bin/bash
DIR=./data/versions/
SCRIPT="./scripts/bioconda-binaries"
OUTDIR="./data/binaries"
mkdir -p "$OUTDIR"
if [[ ! -e "$SCRIPT" ]]; then
  echo "ERROR: Missing single package script $SCRIPT"
  exit 1
fi

echo "Will used files in $DIR"

for file in "$DIR"/*.txt;
do
  if [[ ! -e "$file" ]]; then
      echo "ERROR: $file not found"
      continue
  fi
  package=$(basename ${file%.txt});
  echo $package;
  for ver in $(cat $file);
  do
     echo " - $ver";
     $SCRIPT  --flexible -o "$OUTDIR" --verbose  ${package}=${ver}
  done;
done
