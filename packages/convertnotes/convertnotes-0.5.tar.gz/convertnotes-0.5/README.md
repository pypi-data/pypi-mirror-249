# ConvertNotes

This tool converts your notes from one format/application to another. Currently, the only supported conversion is from *Logseq* to *Roam*.

## Features

The primary reason to use this suite of tools is that it does the following:
- Preserves block references
- Fixes date formatting (Daily Notes will work)
- Converts Logseq properties to Roam attributes
- Enables uploading assets (images, pdfs, etc) and preserving the links to those assets in your knowledge graph
- Removes unecessary Logseq metadata (image sizes, logbook, etc)

This makes the transition from Logseq to Roam as seamless as possible.

### Important Note

While I have tested this rather extensively with my own notes, it is entirely possible that I have forgotten something or made a mistake. Use these tools at your own risk and make sure you have everything backed up in case something goes wrong.

## Installation

```sh
$ pip install convertnotes
```

## Upload Assets to Roam Research

Roam does not provide a convenient way to upload images, however it does allow you to run somewhat arbitrary Javascript which can do the trick.

To do this, first you need to enable "user code" in your User settings:

![](./assets/user_code_option.png)

Then copy [this snippet](./assets/upload.txt) and paste it anywhere in your Roam notes.

When you do this, it will give you a warning like this:

![](./assets/warning.png)


Click the button that says you know what you are doing and then restart your Roam graph (restart the app, refresh the page, etc) to make sure that the javascript loads.

Once it restarts, run the keyboard shortcut `cmd+p` to open the command palette. Now just search for "ConvertNotes" and you should see an option like the following:

![](./assets/convertnotes.png)

Hit the `Enter` key. You will now be prompted to select the files you want to upload. If you are coming from logseq, the files you're looking for are in the `assets` directory within your graph folder.

Select *all* of the files that you want which are referenced in your notes and wait for them to upload. *Do not navigate or do anything.* It might take a while because the files are uploaded in batches. Once they are done you will be prompted to download a **metadata JSON file**. Save this. You will need it when running `convertnotes` so that the links in your notes can be updated to reference the new files managed by Roam.

## Usage

To export your notes from Logseq and import them into Roam, first export your notes as JSON from within Logseq (see [docs](https://docs.logseq.com/#/page/export)). Once you have the JSON file, navigate to the file in your terminal and execute a command like the following to convert them to Roam JSON:

```sh
$ convertnotes \
    --inputfile ./logseq.json \
    --outputfile ./roam.json \
    --metadatafile ./metadata.json \
    --profile logseqtoroam
```

Then open up Roam, and import the resulting JSON file.
