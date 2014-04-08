import csv
import json

def write_json(stargazers, out):
    return json.dump([ s.to_json() for s in stargazers ], out)

def write_tablular(sep):
    def writer(stargazers, out):
        fieldnames = sorted(stargazers[0].to_json().keys(),
            key=len)
        writer = csv.DictWriter(out,
            delimiter=sep,
            fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([ s.to_json() for s in stargazers ])
    return writer

write_csv = write_tablular(",")
write_tsv = write_tablular("\t")
