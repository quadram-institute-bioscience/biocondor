# BioCondor (alpha)

[![biocondor logo](docs/biocondor-logo.png)](https://corebio.info/biocondor)

Retrieve, cache and search for bioconda packages and their descriptions.

:globe_with_meridians: **Website**: [corebio.info/biocondor](https://corebio.info/biocondor)

## Background

[Bioconda](https://bioconda.github.io/) is a distribution of bioinformatics software packaged for the conda package manager, hosting thousands of tools used in genomics, transcriptomics, proteomics, and related fields. Finding the right tool — or understanding what a package does — often requires browsing multiple sources.

BioCondor addresses this by locally caching bioconda package metadata (fetched from the Anaconda and GitHub APIs) and exposing fast, regex-powered search across package names, descriptions, and other fields. 

A script based on the installation of the package **extracts the list of binaries** specific to each package. This can be viewed online (example, the [subread package](https://corebio.info/biocondor/package.html?package=subread)).

## Scripts

| Script | Purpose |
|---|---|
| `getBiocondaCache.py` | Download and cache all bioconda package metadata |
| `grep_conda.py` | Search cached packages with regex |
| `package_info.py` | Display detailed info for a specific package |
| `get_field.py` | Extract a specific field across all packages |
| `bioconda-get-binaries.py` | Retrieve binary package information |

## Documentation

:warning: This repository contains a preliminary version of BioCondor.

Full documentation is in the :book: [repository wiki](https://github.com/quadram-institute-bioscience/biocondor/wiki).
