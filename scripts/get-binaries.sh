#!/bin/bash
for file in versions/*.txt;
do
  package=$(basename ${file%.txt});
  echo $package;
  for ver in $(cat $file);
  do
     echo " - $ver";
     bioconda-binaries  --flexible -o binaries --verbose  ${package}=${ver}
  done;
done
