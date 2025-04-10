# Download VC Photos

## Description

This repository contains a Python scripts for downloading user photos from Veracross. Source CSV file is supplied as a list of peson_id and photo_url columns. The script reads and downloads these one by one into the specified directory. This script can be set on a scheduled job to nightly pull all photos or as desired.

## Setup

1. **Clone the Repository:**

```sh
git clone [repository-url]
cd [repository-name]
```

2. **Install Dependencies:**

```sh
pip install -r requirements.txt
```

## Usage

To run the script manually:

```sh
python3 download_with_renaming.py
```