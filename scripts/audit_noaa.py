#!/usr/bin/env python
"""Bounded SanctSound TOL hourly feasibility audit; no interpolation or modeling."""
import argparse, csv, hashlib, json, urllib.request, datetime, sys
from pathlib import Path

CANDIDATES = {
    "SB02_07": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/noaaSanctSound_SB02_07_TOL.html",
    "FK03_04": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/noaaSanctSound_FK03_04_TOL.html",
    "PM02_01": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/noaaSanctSound_PM02_01_TOL.html",
}

def fetch(url, timeout=20):
    req=urllib.request.Request(url, headers={"User-Agent":"DS-A5-feasibility-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.status

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out', default='data/manifest.json')
    ap.add_argument('--sample-days', type=int, default=90)
    a=ap.parse_args(); entries=[]
    for site, url in CANDIDATES.items():
        item={"station":site,"metadata_url":url,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"UNVERIFIED"}
        try:
            body,status=fetch(url+'.json')
            item.update(status="ACCESSIBLE",http_status=status,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
            item["dataset_json"]=json.loads(body.decode('utf-8'))
        except Exception as e:
            item.update(status="BLOCKED",error=f"{type(e).__name__}: {e}")
        entries.append(item)
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps({"generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"sample_days":a.sample_days,"candidates":entries},indent=2))
    print(json.dumps(entries,indent=2))
    return 0 if any(x['status']=='ACCESSIBLE' for x in entries) else 2
if __name__=='__main__': sys.exit(main())
