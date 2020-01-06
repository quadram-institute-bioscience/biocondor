# biocondor

Retrieve, cache and search for bioconda packages and their descriptions

## scripts

* **saveBiocondaCache.py** - download JSON files from BioConda: the global list (bioconda.json) and the JSON metadata for each package. If the bioconda.json is recent, it won't be downloaded. If the package version is equal to the version in bioconda.json, it won't be downloaded.
* **biocondor.py** - search a package using a downloaded cache
