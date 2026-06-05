import csv
from Evtx.Evtx import Evtx

def import_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            yield line.strip()

def import_csv(file_path):
    with open(file_path, newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

def import_evtx(file_path):
    with Evtx(file_path) as log:
        for record in log.records():
            yield record.xml()