"""Linux inotify observation of synthetic archive opens; no source-content reads.

Monitor only explicitly assigned synthetic directories. An open/access event does
not prove comprehension or provider identity. Stop before evaluator source reads.
"""
import argparse
import ctypes
import json
import os
from pathlib import Path
import struct
import time


def monitor(paths, out, stop_file):
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
    if fd < 0: raise OSError(ctypes.get_errno(), 'inotify initialization failed')
    watches = {}
    try:
        for path in paths:
            wd = libc.inotify_add_watch(fd, os.fsencode(path), 0x1 | 0x10 | 0x20 | 0x4000)
            if wd < 0: raise OSError(ctypes.get_errno(), 'inotify watch failed')
            watches[wd] = str(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x') as log:
            log.write(json.dumps({'event':'ready','directories':list(watches.values()),'monotonic_seconds':time.monotonic()})+'\n');log.flush()
            while not stop_file.exists():
                try: data = os.read(fd, 1024*1024)
                except BlockingIOError:
                    time.sleep(0.1);continue
                offset = 0
                while offset < len(data):
                    wd, mask, cookie, size = struct.unpack_from('iIII', data, offset)
                    name = data[offset+16:offset+16+size].split(b'\0',1)[0].decode()
                    offset += 16+size
                    log.write(json.dumps({'directory':watches.get(wd),'name':name,'mask':mask,
                        'opened':bool(mask & 0x20),'accessed':bool(mask & 0x1),
                        'queue_overflow':bool(mask & 0x4000),'monotonic_seconds':time.monotonic()})+'\n')
                log.flush()
            log.write(json.dumps({'event':'stopped','monotonic_seconds':time.monotonic()})+'\n')
    finally: os.close(fd)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--watch',type=Path,action='append',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--stop-file',type=Path,required=True)
    a=p.parse_args();monitor(a.watch,a.out,a.stop_file)


if __name__=='__main__':main()
