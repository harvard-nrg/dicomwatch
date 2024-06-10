DICOM Watch will monitor a directory for `tar` archives. Any `tar` archives 
that appear within the watched directory are assumed to contain 
[DICOM-formatted](https://www.dicomstandard.org/) files that should be sent 
to a DICOM C-STORE Service Class Provider (DICOM SCP).

## Installation
Just use `pip`

```bash
pip install git+https://github.com/harvard-nrg/dicomwatch.git
```

This software has been tested on macOS Sonoma (arm64) and Linux (amd64) using 
Python 3.11.

## Usage
> [!NOTE]
> This example assumes that `scp.example.org` is the target DICOM SCP with AE
> title `ANY-SCP` and listening on port `11112`.

```bash
start.py --hostname scp.example.org --port 11112 --ae-title ANY-SCP --folder /location
```

## How it works
This software uses [`watchdog`](https://github.com/gorakhargosh/watchdog) to watch
a directory for gzipped `tar` archives i.e., files ending in `.tar.gz`. 

When a `tar` archive appears within the watched directory, the software will inspect 
the archive for any DICOM-formatted files and send those files to the specified 
DICOM SCP using [`pynetdicom`](https://github.com/pydicom/pynetdicom).

## Can I watch cloud storage?
The user supplied `--folder` can be any local directory. If you want to watch a directory
that lives in the cloud, you should consider mounting your cloud storage using 
[`rclone mount`](https://rclone.org/commands/rclone_mount/).
