# Zotero2reMarkable Bridge

This program can be used to sync attachments from Zotero to your ReMarkable
*and* sync them back to Zotero again.

It relies on both Zotero's and reMarkable's cloud APIs for Python. This means
sync must be enabled in Zotero to use this program. Both Zotero's storage and external WebDAV storage is supported, 
although Zotero's own cloud support is largely untested. Testing and bug reports/pull requests are highly appreciated.

## Usage

The workflow starts at Zotero. To pick which attachment to sync, add the `to_sync` tag to the entry.

When you run the script, these files will be synced to your "unread" folder on the reMarkable.

Once you're done reading and/or annotating, move the notebook from "unread" to "read" on your tablet.

Now, when you run the script again, your annotations will be synced back to zotero.

### How it works

To designate attachments that should be synced, add the tag "to_sync" to the entry.

After the files are synced, this tag is automatically removed and set to "synced".
Do not remove these tags as they are used to determine which files should be synced back.

The program uses [remarks](https://github.com/Scrybbling-together/remarks.git) to render files from ReMarkable and therefore has support both for annotations and smart highlights. Colors are supported.

The program will preserve the original file and add the marked file as new attachment with "(Annot) " added in front of the file name.
Entries that have been synced back will have the tag "read" added to them, so you can easily search for them.

- Supports sync via the ReMarkable API

### Setup

#### On reMarkable:

- Create a folder named `Zotero` through the UI on your reMarkable. This folder must be on the top level of the file system and cannot be nested under other folders.
- Create two folders inside the `Zotero` folder, one for your unread documents (this is where new files from Zotero will land) and your read documents (this is where the program looks for files to be synced back to Zotero). 

#### On your PC:

```bash
# 1. Clone repository to your computer:
git clone https://github.com/Scrybbling-together/zotero2remarkable_bridge.git

# Note: The program requires rmapi to be installed and properly configured. Please refer to rmapi's [Readme](https://github.com/ddvk/rmapi/blob/master/README.md) for instructions.

# requires poetry to install
# https://python-poetry.org/
# 2. Add required packages through pip:
poetry install
poetry env use

# 4. On Linux, run the program with:
python ./zotero2remarkable_bridge.py

# At first run, it will guide you through creating a working
# config. It will help you setup authentication with Zotero, WebDAV (optional), and
# ReMarkable.
```

### Arguments

The program accepts the following arguments:

```
./zotero2remarkable_bridge.py [-m push|pull|both]

-m: Mode
push: Only push to ReMarkable

pull: Only pull from ReMarkable and sync to Zotero

both: Go both ways, adding new files to ReMarkable and syncing back
        to ReMarkable.
        
Defaults to "both".
```
