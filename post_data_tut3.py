import requests
import os
import json
import pprint

files = ["resource-examples/Patient-f001.json",
         "resource-examples/Encounter-f001.json",
         "resource-examples/ProcedureRequest-f001.json",
         "resource-examples/Observation-f001.json",
         "resource-examples/Observation-f002.json",
         "resource-examples/DiagnosticReport-f001.json"]


def upload_fhir_data():
    data = []
    for f in files:
        _type = os.path.basename(f).split('-')[0]
        with open(f) as f0:
            tmp = json.load(f0)
        data.append((_type, tmp))

    URL = "https://stu3.test.pyrohealth.net/fhir"

    FHIRJSONMimeType = 'application/fhir+json'
    header_defaults = {
                'Accept': FHIRJSONMimeType,
                'Accept-Charset': 'UTF-8' }

    rids = []

    for d in data:
        print(d[0])
        r = requests.post(URL+"/%s"%d[0], json = d[1],
                           headers = header_defaults)
        if r.ok:
            rids.append((d[0], r.json()["id"]))
        else:
            rids.append((d[0], r.json()['issue'][0]['details']))

    return rids

if __name__ == '__main__':
    rids = upload_fhir_data()
    pp = pprint.PrettyPrinter(indent=2)
    for r in rids:
        print(r[0])
        pp.pprint(r[1])
        print('-'*27)
