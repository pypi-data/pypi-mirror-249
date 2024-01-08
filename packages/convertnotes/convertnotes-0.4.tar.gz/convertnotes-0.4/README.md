# convertnotes

This tool converts your notes from one format/application to another. Currently, the only supported conversion is from Logseq to Roam.

## Installation

```sh
$ pip install convertnotes
```

## Roam Upload

Roam does not provide a convenient way to upload images, however it does allow you to run somewhat arbitrary Javascript which can do the trick.

To do this, first you need to enable "user code" in your User settings:

![](./assets/user_code_option.png)

Then copy the following snippet and paste it anywhere in your Roam notes:

<details>

- {{[[roam/js]]}}
    - ```javascript
async function convertNotesUploader() {
  var batchSize = 4;

  // helper functions
  var downloadJSON = (blob, filename) => {
    // Create a link element
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    // Clean up by revoking the Object URL and removing the link element
    URL.revokeObjectURL(url);
    a.remove();
  }

  function batchArray(arr, size) {
    let result = [];
    for (let i = 0; i < arr.length; i += size) {
      let batch = arr.slice(i, i + size);
      result.push(batch);
    }
    return result;
  }

  // create upload command
  await window.roamAlphaAPI.ui.commandPalette.addCommand({
    label: "Upload images for ConvertNotes",
    callback: () => {
      var fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.id = 'filePicker';
      fileInput.multiple = 'multiple';
      fileInput.display = 'none';
      document.body.appendChild(fileInput);

      fileInput.addEventListener('change', async function (event) {
        var files = event.target.files;
        var batches = batchArray(Array.from(files), batchSize);

        var metadataList = [];

        // upload files in batches
        for (var batch of batches) {
          var batchMetadata = await Promise.all(batch.map(async file => {
            var markdownLink = await roamAlphaAPI.file.upload({ file: file })
            return {
              name: file.name,
              size: file.size,
              type: file.type,
              path: file.path,
              markdownLink: markdownLink,
            }
          }));

          metadataList.push(batchMetadata)
        }

        console.log(metadataList);

        const jsonBlob = new Blob(
          [JSON.stringify(metadataList.flat(), null, 2)],
          { type: 'application/json' }
        );

        downloadJSON(jsonBlob, 'file_metadata.json');

        fileInput.remove();
      });

      fileInput.click();
    },
  });

  console.log("convertnotes loaded");
}

convertNotesUploader();
```

</details>

When you do this, it will give you a warning like this:

![](./assets/warning.png)


Click the button that says you know what you are doing and then restart your Roam graph (restart the app, refresh the page, etc) to make sure that the javascript loads.

Once it restarts, run the keyboard shortcut `cmd+p` to open the command palette. Now just search for "ConvertNotes" and you should see an option like the following:

![](./assets/convertnotes.png)

Hit the `Enter` key. You will now be prompted to select the files you want to upload. If you are coming from logseq, the files you're looking for are in the `assets` directory within your graph folder.

Select *all* of the files that you want which are referenced in your notes and wait for them to upload. *Do not navigate or do anything.* It might take a while because the files are uploaded in batches. Once they are done you will be prompted to download a metadata JSON file. Save this. You will need it when running `convertnotes` so that the links in your notes can be updated to reference the new files managed by Roam.

## Usage

To export your notes from Logseq and import them into Roam, first export your notes as JSON from within Logseq (see [docs](https://docs.logseq.com/#/page/export)). Once you have the JSON file, navigate to the file in your terminal and execute a command like the following to convert them to Roam JSON:

```sh
$ convertnotes -i ./logseq.json -o ./roam.json -p logseqtoroam
```

