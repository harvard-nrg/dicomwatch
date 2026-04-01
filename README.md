# DICOM Watch

DICOM Watch will watch a directory for `tar.gz` files. Any `tar.gz` files
that appear within the directory are assumed to contain 
[DICOM](https://www.dicomstandard.org/) files that will be sent 
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

### forever mode

By default, `dicomwatch` will scan the supplied `--folder` one time, process 
any `tar.gz` files it finds, then it will exit. If you want `dicomwatch` to 
run continuously ("daemon mode"), simply pass the `--forever` argument

```bash
start.py --forever [...]
```

### setting a project

You can have `dicomwatch` set the Study Description `(0008, 1030)` within 
each DICOM file to a custom value. This is useful when sending DICOM files 
to an XNAT installation where you want the data to be auto-archived into a 
particular project

```bash
start.py --project MyProject [...]
```

## How it works

`dicomwatch` uses [`watchdog`](https://github.com/gorakhargosh/watchdog) to watch
a directory for gzipped `tar` archives i.e., files ending in `.tar.gz`. 

When a `tar.gz` appears within the watched directory, the software will inspect 
the archive for any DICOM-formatted files and send those files to the specified 
DICOM SCP using [`pynetdicom`](https://github.com/pydicom/pynetdicom).

## Can I watch cloud storage?

Sure! If you want `dicomwatch` to watch a directory that lives in the cloud, 
you can always mount your cloud storage using a tool like 
[`rclone mount`](https://rclone.org/commands/rclone_mount/).

