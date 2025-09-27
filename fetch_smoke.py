# SMOKE TEST: unduh 1 tanggal, 1 member, 2 lead; crop Jawa Barat; tanpa filter variabel
from pathlib import Path
import pandas as pd
import subprocess, shlex
from herbie import Herbie

DATE = "2019-01-01"   # 1 Jan 2019
CYCLE = "00"
MEM   = "c00"
LEADS = [6, 12]       # f006 & f012 (pasti ada akumulasi)

# BBox Jawa Barat (Banten+DKI+Jabar)
LON_MIN, LON_MAX = 105.0, 109.8
LAT_MIN, LAT_MAX = -7.8, -5.5

OUT_DIR = Path("data/wjava_nc"); OUT_DIR.mkdir(parents=True, exist_ok=True)

def run(cmd: str):
    print(">>", cmd)
    subprocess.run(shlex.split(cmd), check=True)

run_time = pd.Timestamp(f"{DATE} {CYCLE}:00")

for fxx in LEADS:
    H = Herbie(run_time, model="gefs", product="atmos.5", member=MEM, fxx=fxx)
    grib = Path(H.download())
    sub_grib = Path(f"data/wjava_nc/{DATE}_{CYCLE}z_{MEM}_f{fxx:03d}_wjava.grib2")
    out_nc   = Path(f"data/wjava_nc/{DATE}_{CYCLE}z_{MEM}_f{fxx:03d}_wjava.nc")

    # crop bbox (tanpa filter variabel → dijamin ada isi)
    run(f"wgrib2 {grib} -small_grib {LON_MIN}:{LON_MAX} {LAT_MIN}:{LAT_MAX} {sub_grib}")
    # konversi ke NetCDF
    run(f"wgrib2 {sub_grib} -netcdf {out_nc} -nc4 -nc_nlev 1")
