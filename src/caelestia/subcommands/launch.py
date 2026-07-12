import sys
import subprocess
from argparse import Namespace

class Command:
    def __init__(self, args: Namespace):
        self.args = args

    def run(self):
        args_list = getattr(self.args, 'args', [])
        if not args_list:
            print("Usage: caelestia launch [query] <number>")
            sys.exit(1)
            
        if len(args_list) == 1:
            query = ""
            number = args_list[0]
        else:
            query = " ".join(args_list[:-1])
            number = args_list[-1]
            
        try:
            index = int(number)
        except ValueError:
            print("Please provide a valid number.")
            sys.exit(1)
            
        if index < 1:
            print("Index must be 1 or greater.")
            sys.exit(1)
            
        # Call the Quickshell IPC endpoint
        try:
            subprocess.run(["qs", "-c", "caelestia", "ipc", "call", "launcher", "launch", query, str(index)])
        except FileNotFoundError:
            print("Error: Quickshell (qs) is not installed or not in PATH.")
            sys.exit(1)
