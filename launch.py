"""One-click local application supervisor. Uses only loopback network listeners."""
import json, os, pathlib, subprocess, sys, time, urllib.request, webbrowser

ROOT=pathlib.Path(__file__).resolve().parent
DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
URL='http://127.0.0.1:8787'

def health(url):
    try:
        with urllib.request.urlopen(url,timeout=1) as r:return json.load(r)
    except Exception:return None

def run():
    existing=health(URL+'/health')
    if existing:
        if existing.get('app')!='clientdesk':raise RuntimeError('Port 8787 is already occupied by another application')
        if '--headless' not in sys.argv:webbrowser.open(URL)
        return
    app=None
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    py=pathlib.Path(sys.executable)
    if py.name.lower()=='pythonw.exe':py=py.with_name('python.exe')
    with (DATA/'app.log').open('a',encoding='utf-8') as log:
        app=subprocess.Popen([str(py),str(ROOT/'app.py')],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=log,creationflags=flags)
    (DATA/'processes.json').write_text(json.dumps({'supervisor':os.getpid(),'app':app.pid,'ai':'omniroute-server-side'}),encoding='utf-8')
    for _ in range(60):
        if app.poll() is not None:raise RuntimeError('ClientDesk stopped during startup. See data/app.log')
        if health(URL+'/health'):break
        time.sleep(.25)
    if '--headless' not in sys.argv:webbrowser.open(URL)
    app.wait()

if __name__=='__main__':
    try:run()
    except Exception as e:
        (DATA/'launcher-error.txt').write_text(str(e),encoding='utf-8')
        if os.name=='nt' and '--headless' not in sys.argv:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0,str(e),'ClientDesk could not start',0x10)
        raise
