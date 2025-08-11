# Package JSON File Structure

This document describes the structure of the JSON files that contain information about each package.

## Root Level Fields

| Key               | Type    | Description                                                                                             |
| ----------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| `app_entry`       | Object  | Application entry points.                                                                               |
| `app_summary`     | Object  | Application summary.                                                                                    |
| `app_type`        | Object  | Application type.                                                                                       |
| `builds`          | Array   | A list of available build strings for the package.                                                      |
| `conda_platforms` | Array   | A list of conda platforms where the package is available (e.g., `osx-64`, `linux-64`).                  |
| `created_at`      | String  | The timestamp when the package was created.                                                             |
| `description`     | String  | A detailed description of the package.                                                                  |
| `dev_url`         | String  | URL for the development repository of the package.                                                      |
| `doc_url`         | String  | URL for the package's documentation.                                                                    |
| `files`           | Array   | A list of file objects, each representing a specific build and version of the package.                  |
| `full_name`       | String  | The full name of the package, including the owner (e.g., `bioconda/bwa`).                               |
| `home`            | String  | The URL of the package's homepage.                                                                      |
| `identity`        | String  | The identity of the package.                                                                            |
| `license`         | String  | The license of the package.                                                                             |
| `license_url`     | String  | URL to the license file.                                                                                |
| `name`            | String  | The name of the package.                                                                                |
| `owner`           | String  | The owner of the package (e.g., `bioconda`).                                                            |
| `package_types`   | Array   | A list of package types (e.g., `conda`).                                                                |
| `platforms`       | Array   | A list of platforms where the package is available.                                                     |
| `public`          | Boolean | A boolean indicating if the package is public.                                                          |
| `revision`        | Number  | The revision number of the package metadata.                                                            |
| `source_git_url`  | String  | The git URL for the source code of the package.                                                         |
| `source_git_tag`  | String  | The git tag for the source code of the package.                                                         |
| `summary`         | String  | A brief summary of the package.                                                                         |
| `updated_at`      | String  | The timestamp when the package was last updated.                                                        |
| `versions`        | Array   | A list of all available versions of the package.                                                        |

---

## The `files` Array

The `files` array contains objects, where each object represents a downloadable file for the package.

| Key                 | Type   | Description                                                                                              |
| ------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| `attrs`             | Object | An object containing various attributes of the file.                                                     |
| `basename`          | String | The filename of the package archive (e.g., `linux-64/bwa-0.7.17-pl5.22.0_2.tar.bz2`).                     |
| `dependencies`      | Object | An object describing the dependencies of the package.                                                    |
| `description`       | String | A description of the file (often `null`).                                                                |
| `distribution_type` | String | The type of distribution (e.g., `conda`).                                                                |
| `download_url`      | String | The URL to download the package file.                                                                    |
| `full_name`         | String | The full name of the file, including owner and version information.                                      |
| `labels`            | Array  | A list of labels associated with the file (e.g., `main`, `cf201901`).                                    |
| `md5`               | String | The MD5 hash of the file.                                                                                |
| `ndownloads`        | Number | The number of times the file has been downloaded.                                                        |
| `owner`             | String | The owner of the package.                                                                                |
| `sha256`            | String | The SHA256 hash of the file.                                                                             |
| `size`              | Number | The size of the file in bytes.                                                                           |
| `type`              | String | The type of the file (e.g., `conda`).                                                                    |
| `upload_time`       | String | The timestamp when the file was uploaded.                                                                |
| `version`           | String | The version of the package in this file.                                                                 |

### The `files.attrs` Object

| Key               | Type    | Description                                                                |
| ----------------- | ------- | -------------------------------------------------------------------------- |
| `arch`            | String  | The architecture of the build (e.g., `x86_64`).                            |
| `build`           | String  | The build string.                                                          |
| `build_number`    | Number  | The build number.                                                          |
| `depends`         | Array   | A list of dependencies for the build.                                      |
| `has_prefix`      | Boolean | A boolean indicating if the package has a prefix.                          |
| `license`         | String  | The license of the build.                                                  |
| `machine`         | String  | The machine type (e.g., `x86_64`).                                         |
| `operatingsystem` | String  | The operating system of the build (e.g., `linux`, `darwin`).               |
| `platform`        | String  | The platform of the build (e.g., `linux`, `osx`).                          |
| `subdir`          | String  | The subdirectory for the build (e.g., `linux-64`).                         |
| `target-triplet`  | String  | The target triplet for the build (e.g., `x86_64-any-linux`).               |
| `timestamp`       | Number  | The timestamp of the build.                                                |

### The `files.dependencies` Object

| Key       | Type  | Description                                           |
| --------- | ----- | ----------------------------------------------------- |
| `depends` | Array | A list of dependency objects for the file.            |

#### The `files.dependencies.depends` Array

| Key     | Type   | Description                                      |
| ------- | ------ | ------------------------------------------------ |
| `name`  | String | The name of the dependency.                      |
| `specs` | Array  | A list of version specifications for the dependency. |
