#!/usr/bin/env python

#
# Convert AmiPro CMZ Archives into DCL Implode and extract
# them with deark.
#
# https://github.com/sourcekris/uncmz
#
# Requires: https://github.com/jsummers/deark
#

import argparse
import sys
import shutil
import os, os.path
import subprocess
import tempfile
from struct import unpack

file_sig = b'Clay'
crcoff = 0xc
fnszoff = 0x10
fnoff = 0x14

def main(argv):
    ap = argparse.ArgumentParser(description="Extract Lotus CMZ Files.", 
                                 epilog="Please file bugs on the GitHub Issues. Thanks")
    ap.add_argument("-e", "--extract", required=True, help="The CMZ file to extract.", metavar="FILENAME")
    ap.add_argument("-d", "--destination", help="An optional output folder.", metavar="PATH")
    ap.add_argument("-p", "--deark", help="Path to deark archiver in case it is not in $PATH", metavar="PATH")
    args = ap.parse_args(argv)
    
    fn = args.extract
    if not os.path.exists(fn):
        print(f"{fn} does not exist.")
        return
    
    if args.destination and not os.path.isdir(args.destination):
        print(f"destination folder {args.destination} does not exist")
        return

    with open(fn, "rb") as f:
        id = f.read(4)
        if id != file_sig:
            print(f'{fn} does not appear to be a CMZ file')
            return

        compsize = unpack('I', f.read(4))[0]
        uncompsize = unpack('I', f.read(4))[0]
        print(f'compressed size:\t{compsize} bytes')
        print(f'uncompressed size:\t{uncompsize} bytes')

        f.seek(fnszoff)
        fnsz = ord(f.read(1))

        if fnsz > 12:
            print(f'invalid filename size {fnsz}')
            return

        f.seek(fnoff)
        fname = f.read(fnsz).decode()
        print(f"compressed filename:\t{fname}")

        if args.destination:
            fname = os.path.join(args.destination, fname)

        if os.path.exists(fname):
            print(f"aborted: {fname} file exists, choosing not to overwrite it")
            return
        
        compdata = f.read(compsize)

        with tempfile.NamedTemporaryFile() as dclfile:
            open(dclfile.name, 'wb').write(compdata)

            deark = "deark"
            if args.dearkpath:
                if os.path.exists(args.dearkpath):
                    if os.path.isfile(args.dearkpath):
                        deark = args.dearkpath
                    
                    if os.path.isdir(args.dearkpath) and os.path.isfile(os.path.join(args.dearkpath, deark)):
                        deark = os.path.join(args.dearkpath, deark)
                
                if deark == "deark":
                    print(f"deark not found at path {args.dearkpath} so aborting.")
                    return
            with tempfile.NamedTemporaryFile(delete=False) as uncfile:
                cmdline = [deark, '-m', 'dclimplode',dclfile.name, '-o', uncfile.name]
                outs = errs = ""
                try:
                    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    outs, errs = p.communicate()
                except Exception as e:
                    print(f"failed extracting the DCL portion of the file: {e}")
                    return

                extracted = uncfile.name + ".000.unc"
                if os.path.isfile(extracted):
                    shutil.move(extracted, fname)
                    print(f"wrote {fname}")

                else:
                    print(f"failed extracting with deark: {outs} {errs}")
                    return

        



if __name__ == "__main__":
    main(sys.argv[1:])