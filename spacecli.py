#!/usr/bin/env python3
import spaceapi
import argparse
import json

def resolve(obj, path):
    for p in path:
        obj = obj[p]
    return str(obj)

def print_objs(headers, objects, subs=[]):
    for h in headers:
        print(f"{h:<{headers[h].get('width', 15)}}",end="")
    print()
    for obj in objects["data"]:
        for h in headers:
            print(f"{resolve(obj,headers[h]['path']):<{headers[h].get('width', 15)}}", end="")
        print()
        for sub_key in subs:
            sub_objects = obj[sub_key]
            for subobj in sub_objects:
                print("  ", end="")
                subheaders = subs[sub_key]
                for subh in subheaders:
                    print(f"{resolve(subobj, subheaders[subh]['path']):<{subheaders[subh].get('width', 15)}}", end="")
                print()
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
                "System": {
                    "path": ("symbol",),
                    "width": 30
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
                    "path": ("symbol",),
                    "width": 30
                },
                "Type": {
                    "path": ("type",),
                    "width": 30
                },
                "X": {
                    "path": ("x",),
                    "width": 6,
                },
                "Y": {
                    "path": ("y",),
                    "width": 6,
                }
        }
    wayheaders = {
                "Id": {
                    "path": ("symbol",),
                    "width": 28
                },
                "Type": {
                    "path": ("type",),
                    "width": 30
                },
                "X": {
                    "path": ("x",),
                    "width": 6,
                },
                "Y": {
                    "path": ("y",),
                    "width": 6,
                }
        }
    print_objs(headers, spaceapi.systems(), subs={
        "waypoints": wayheaders})

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
    if hasattr(options, "command") == None:
        parser.print_help()
        return
    options.command(options)

main()
