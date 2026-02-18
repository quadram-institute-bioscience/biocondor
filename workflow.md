## Initialise

```bash
mkdir -p data/{versions,binaries,downloads}
```

## Get repository

To have an updated list of "recipes". 
APIs are unreliable given the number of directories and this is realiable enough.

```bash
git clone git@github.com:bioconda/bioconda-recipes.git

#or
cd bioconda-recipes
git pull
cd -
```

### Get cache with script


```bash
python scripts/getBiocondaCache.py 
```

This produces "./biocondor_cache/*.json"

TODO: 
```bash
cp biocondor_cache/*.json docs/bioconda_cache/
```

## Get package versions

```bash
./scripts/bioconda-fetch-version  \
  -s scripts/bioconda-versions  \
  -o data/versions/ bioconda-recipes/recipes/
```

## Get binaries


```bash
bash scripts/get-binaries.sh
```
---

# Website update

"./docs" is a github pages searchable website.


Requires:
* "./docs/binaries"
* "./docs/bioconda_cache"
