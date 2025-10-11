#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'generator' / 'template.html'


def run(cmd, cwd=None, check=True):
    print(f"Running: {cmd} (cwd={cwd})")
    subprocess.run(cmd, shell=True, check=check, cwd=cwd)


def comment_base():
    cmd = "sed -Ei 's|^([[:space:]]*)(<base[^>]*>)|\\1<!--\\2 -->|' \"{}\"".format(TEMPLATE)
    run(cmd)


def uncomment_base():
    cmd = "sed -Ei 's|^([[:space:]]*)<!--[[:space:]]*(<base[^>]*>)[[:space:]]*-->|\\1\\2|' \"{}\"".format(TEMPLATE)
    run(cmd)


def do_generate():
    run('python3 generate.py', cwd=str(ROOT / 'generator'))


def start_php():
    php_cmd = ['php', '-S', '127.0.0.1:8000', '-t', str(ROOT)]
    # start in a new process group so we can kill tree later
    proc = subprocess.Popen(php_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            preexec_fn=os.setsid)
    print(f"Started php (pid={proc.pid})")
    return proc


def open_browser():
    url = 'http://127.0.0.1:8000/index.php'
    browser = os.environ.get('BROWSER')
    if browser:
        cmd = [browser, url]
    else:
        # use xdg-open on Linux (works in most dev containers)
        cmd = ['xdg-open', url]
    try:
        subprocess.Popen(cmd)
    except Exception:
        print('Failed to open browser with', cmd)


def main():
    proc = None

    def stop(signum, frame):
        print('Stopping...')
        if proc and proc.poll() is None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    comment_base()
    try:
        do_generate()
    finally:
        # always restore template regardless of generator result
        uncomment_base()

    proc = start_php()
    open_browser()

    # wait until php process exits or we receive signal
    try:
        while True:
            ret = proc.poll()
            if ret is not None:
                print('PHP server exited with', ret)
                break
            signal.pause()
    except KeyboardInterrupt:
        stop(None, None)


if __name__ == '__main__':
    main()
