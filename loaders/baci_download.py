"""
loaders/baci_download.py
---------------------------------------------------------------------------
Downloads one BACI release from CEPII, unzips it, and (optionally) runs the
loader straight afterwards.

What it does, step by step
  1. Reads the CEPII BACI page and finds the newest version number
     (e.g. 202601) by looking for links named BACI_HS92_V202601.zip.
  2. Downloads the zip for each HS revision you ask for into
     data/raw/baci/<today>/zips/   (skips a zip that is already complete).
  3. Unzips everything into data/raw/baci/<today>/ and writes manifest.json
     (what was downloaded, from where, when, and a checksum).
  4. With --load, runs loaders/baci_load.py on that folder.

Run from the repository root:
    python loaders/baci_download.py                 # HS92 + HS22, newest version
    python loaders/baci_download.py --load          # ... and convert to Parquet
    python loaders/baci_download.py --revisions 92 17 22
    python loaders/baci_download.py --version 202601   # if the page can't be read

Only uses Python's standard library. The HS92 zip is large (gigabytes):
expect a long download, and make sure the disk has room.
"""

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

PAGE_URL = "https://www.cepii.fr/cepii/en/bdd_modele/bdd_modele_item.asp?id=37"
DATA_URL = "https://www.cepii.fr/DATA_DOWNLOAD/baci/data"
USER_AGENT = "GeoGIGA-atlas data loader (research use)"


def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def find_latest_version(html):
    """Return the highest version (e.g. '202601') linked on the CEPII page."""
    versions = re.findall(r"BACI_HS\d{2}_V(\d{6}[a-z]?)\.zip", html)
    if not versions:
        raise RuntimeError("No BACI zip links found on the page. "
                           "CEPII may have changed the page; use --version.")
    return max(versions)


def download(url, target):
    """Download url to target, showing progress. Skip if already complete."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        total = int(response.headers.get("Content-Length") or 0)
        if target.exists() and total and target.stat().st_size == total:
            print(f"  already downloaded: {target.name}")
            return
        partial = target.with_suffix(".part")
        done = 0
        with open(partial, "wb") as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r  {target.name}: {done / total:6.1%} of "
                          f"{total / 1e9:.2f} GB", end="", flush=True)
        print()
        partial.rename(target)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Download and unzip BACI.")
    parser.add_argument("--revisions", nargs="+", default=["92", "22"],
                        help="HS revisions, two digits each (default: 92 22)")
    parser.add_argument("--version", help="e.g. 202601 (default: newest on the page)")
    parser.add_argument("--load", action="store_true",
                        help="run loaders/baci_load.py when done")
    parser.add_argument("--data-url", default=DATA_URL, help=argparse.SUPPRESS)
    args = parser.parse_args()

    version = args.version or find_latest_version(fetch_text(PAGE_URL))
    print(f"BACI version {version}, revisions {', '.join(args.revisions)}")

    snapshot = Path("data/raw/baci") / dt.date.today().isoformat()
    zip_dir = snapshot / "zips"
    zip_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"source": "BACI (CEPII)", "page": PAGE_URL, "version": version,
                "downloaded": dt.datetime.now().isoformat(timespec="seconds"),
                "files": []}

    for rev in args.revisions:
        name = f"BACI_HS{rev}_V{version}.zip"
        url = f"{args.data_url}/{name}"
        target = zip_dir / name
        print(f"Downloading {url}")
        download(url, target)
        print(f"  unzipping into {snapshot}/")
        with zipfile.ZipFile(target) as z:
            z.extractall(snapshot)
        manifest["files"].append({"url": url, "zip": name, "sha256": sha256(target)})

    (snapshot / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Done. Raw files are in {snapshot}/")

    if args.load:
        loader = Path(__file__).with_name("baci_load.py")
        subprocess.run([sys.executable, str(loader), str(snapshot)], check=True)


if __name__ == "__main__":
    main()
