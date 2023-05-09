import spaceapi
import argparse
import json

def resolve(obj, path):
    for p in path:
        obj = obj[p]
    return str(obj)

def print_objs(headers, objects):
    for h in headers:
        print(f"{h:<{headers[h].get('width', 15)}}",end="")
    print()
    for obj in objects["data"]:
        for h in headers:
            print(f"{resolve(obj,headers[h]['path']):<{headers[h].get('width', 15)}}", end="")
        print()

def iships(options):
    if options.json:
        print(json.dumps(spaceapi.ships()))
        return

    headers={
                "CallSign": {
                    "path": ("symbol",)
                },
                "System":{
                    "path": ("nav","systemSymbol")
                },
                "NavStatus":{
                    "path": ("nav", "status")
                }
            }
    print_objs(headers, spaceapi.ships())

def icontracts(options):
    if options.json:
        print(json.dumps(spaceapi.contracts()))
        return
    headers = {
                "Id": {
                    "path": ("id",),
                    "width": 30
                },
                "Faction": {
                    "path": ("factionSymbol",)
                },
                "Deadline": {
                    "path": ("terms", "deadline"),
                    "width": 30
                },
                "Accept ($)": {
                    "path": ("terms", "payment", "onAccepted")
                },
                "Fulfill ($)": {
                    "path": ("terms", "payment", "onFulfilled")
                },
                "Accepted": {
                   "path": ("accepted",) 
                }
            }
    print_objs(headers, spaceapi.contracts())

def isystems(options):
    if options.json:
        print(json.dumps(spaceapi.systems()))
        return
    headers = {
                "Id": {
                    "path": ("id",),
                    "width": 30
                },
                "Faction": {
                    "path": ("factionSymbol",)
                },
                "Deadline": {
                    "path": ("terms", "deadline"),
                    "width": 30
                },
                "Accept ($)": {
                    "path": ("terms", "payment", "onAccepted")
                },
                "Fulfill ($)": {
                    "path": ("terms", "payment", "onFulfilled")
                },
                "Accepted": {
                   "path": ("accepted",) 
                }
            }
    print_objs(headers, spaceapi.contracts())


def iaccept(options):
    print(json.dumps(spaceapi.accept(options.contract_id)))

def main():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(title="commands")
    
    contracts = commands.add_parser("contracts")
    contracts.set_defaults(command=icontracts)
    contracts.add_argument("--json", action="store_true")

    accept = commands.add_parser("accept")
    accept.set_defaults(command=iaccept)
    accept.add_argument("contract_id")

    ships= commands.add_parser("ships")
    ships.set_defaults(command=iships)
    ships.add_argument("--json", action="store_true")

    ships= commands.add_parser("systems")
    ships.set_defaults(command=isystems)
    ships.add_argument("--json", action="store_true")


    options = parser.parse_args()
    options.command(options)

main()
