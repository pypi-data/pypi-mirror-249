# convertnotes

This tool converts your notes from one format/application to another. Currently, the only supported conversion is from Logseq to Roam.

## Installation

```sh
$ pip install convertnotes
```

## Usage

To export your notes from Logseq and import them into Roam, first export your notes as JSON from within Logseq (see [docs](https://docs.logseq.com/#/page/export)). Once you have the JSON file, navigate to the file in your terminal and execute a command like the following to convert them to Roam JSON:

```sh
$ convertnotes -i ./logseq.json -o ./roam.json -p logseqtoroam
```
