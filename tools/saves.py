#!/usr/bin/env python3
"""Backs up the app's saves to the computer, or puts a backup back.

  python tools/saves.py backup [file]     (default: GalaxyQuest-saves-<date>.tar)
  python tools/saves.py restore file

The saves live in the app's private storage on the headset, which only the
app itself can reach (adb run-as, as the APK is debuggable): uninstalling
the app deletes them.  A backup is a tar file of that folder, to keep, or to
restore on another headset (the app installed there first) or after a
reinstall.  Restoring replaces the headset's saves: the app is closed first,
and the saves it had are backed up next to the file restored from.

The headset must be connected over USB with developer mode on, and adb
(Android platform-tools) on PATH or in ADB.  Saves belong to the disc they
were made with: one from the European disc shows up on the European disc
only, one from the American disc on the American one.
"""
import io
import os
import subprocess
import sys
import tarfile
import time

from push_data import PACKAGE, adb_environment, find_adb

SAVES = 'files/nand'  # in the app's data folder, where run-as starts
TMP = '/data/local/tmp/galaxyquest_saves.tar'


def headset(adb, serial):
    command = [adb] + (['-s', serial] if serial else [])
    if serial:
        return command
    devices = subprocess.run([adb, 'devices'], check=True, capture_output=True, text=True,
                             stdin=subprocess.DEVNULL, env=adb_environment()).stdout.split('\n')[1:]
    ready = [line.split()[0] for line in devices if line.strip().endswith('device')]
    if not ready:
        sys.exit('no headset found: connect it over USB, allow USB debugging in the headset, and try again')
    if len(ready) != 1:
        sys.exit('more than one device found: disconnect the others or use --serial SERIAL')
    return [adb, '-s', ready[0]]


def run(command, *args, binary=False):
    result = subprocess.run(command + list(args), stdin=subprocess.DEVNULL, capture_output=True,
                            text=not binary, env=adb_environment())
    if result.returncode != 0:
        err = result.stderr if not binary else result.stderr.decode('utf-8', 'replace')
        out = result.stdout if not binary else b''
        sys.exit('adb %s failed: %s' % (' '.join(args), (err or out).strip()))
    return result.stdout


def save_files(data):
    """The files in a backup's tar data, {path: bytes}; exits if it holds no save."""
    files = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            for m in tar.getmembers():
                if m.isfile():
                    files[m.name] = tar.extractfile(m).read()
                elif not m.isdir() or not m.name.startswith(SAVES):
                    sys.exit('not a saves backup: it holds %s' % m.name)
    except tarfile.TarError as e:
        sys.exit('not a saves backup (%s)' % e)
    if not any(n.startswith(SAVES + '/') and n.endswith('/GameData.bin') for n in files):
        sys.exit('no save in it (no %s/.../GameData.bin)' % SAVES)
    return files


REGIONS = {'P': 'European', 'E': 'American', 'J': 'Japanese', 'K': 'Korean'}


def discs(files):
    """The discs whose saves they are (each has a folder named after its game ID in hex)."""
    names = []
    for n in sorted(files):
        if n.endswith('/GameData.bin'):
            folder = n.split('/')[-3]
            try:
                game = bytes.fromhex(folder).decode('ascii')
            except ValueError:
                game = folder
            names.append('the %s disc' % REGIONS[game[3]] if len(game) == 4 and game[3] in REGIONS else folder)
    return ', '.join(names)


def read_saves(command):
    """The headset's saves as tar data, or None when it has none yet."""
    listing = subprocess.run(command + ['shell', 'run-as', PACKAGE, 'ls', SAVES], stdin=subprocess.DEVNULL,
                             capture_output=True, text=True, env=adb_environment())
    if 'not debuggable' in listing.stdout + listing.stderr or 'unknown package' in listing.stdout + listing.stderr:
        sys.exit('cannot reach the app\'s saves: %s' % (listing.stdout + listing.stderr).strip())
    if listing.returncode != 0:
        return None
    return run(command, 'exec-out', 'run-as', PACKAGE, 'tar', 'cf', '-', SAVES, binary=True)


def backup(command, path):
    data = read_saves(command)
    if data is None:
        sys.exit('the app has no saves on this headset yet')
    files = save_files(data)
    with open(path, 'wb') as f:
        f.write(data)
    print('saved %s (%d bytes; saves of %s)' % (path, len(data), discs(files)))


def restore(command, path):
    with open(path, 'rb') as f:
        data = f.read()
    files = save_files(data)
    run(command, 'shell', 'am', 'force-stop', PACKAGE)  # it would write its own saves over them
    current = read_saves(command)
    if current is not None:
        keep = os.path.join(os.path.dirname(os.path.abspath(path)),
                            'GalaxyQuest-saves-replaced-%s.tar' % time.strftime('%Y%m%d-%H%M%S'))
        with open(keep, 'wb') as f:
            f.write(current)
        print('the headset\'s saves until now: %s' % keep)
    # Over the saves there: those of another disc stay.
    run(command, 'push', path, TMP)
    run(command, 'shell', 'run-as', PACKAGE, 'tar', 'xof', TMP)
    run(command, 'shell', 'rm', '-f', TMP)
    back = read_saves(command)
    there = save_files(back) if back is not None else {}
    if any(there.get(name) != content for name, content in files.items()):
        sys.exit('the saves did not arrive whole: try again')
    print('restored %s (saves of %s)' % (path, discs(files)))


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('action', choices=('backup', 'restore'))
    ap.add_argument('file', nargs='?')
    ap.add_argument('--serial', help='headset serial, as listed by adb devices')
    args = ap.parse_args()
    command = headset(find_adb(), args.serial)
    if args.action == 'backup':
        backup(command, args.file or 'GalaxyQuest-saves-%s.tar' % time.strftime('%Y%m%d-%H%M%S'))
    else:
        if not args.file:
            sys.exit('which backup? python tools/saves.py restore <file>')
        restore(command, args.file)


if __name__ == '__main__':
    main()
