"""Configure an existing OmniRoute endpoint key without printing its value."""
import argparse, getpass, json, os, pathlib, sqlite3, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--from-existing',action='store_true',help='Reuse an active key in this user\'s local OmniRoute database, read-only')
    parser.add_argument('--model',default='auto/best-free')
    parser.add_argument('--base-url',default='http://127.0.0.1:20128/v1')
    args=parser.parse_args()
    key=os.environ.get('OMNIROUTE_API_KEY','')
    if args.from_existing:
        source=pathlib.Path.home()/'.omniroute'/'storage.sqlite'
        with sqlite3.connect('file:'+source.as_posix()+'?mode=ro',uri=True) as c:
            row=c.execute('SELECT key FROM api_keys WHERE is_active=1 AND revoked_at IS NULL ORDER BY created_at LIMIT 1').fetchone()
        if not row or not row[0]:raise SystemExit('No reusable active key found. Create an endpoint key in OmniRoute and configure it manually.')
        key=row[0]
    if not key:key=getpass.getpass('Existing OmniRoute endpoint key: ')
    req=urllib.request.Request(args.base_url.rstrip('/')+'/models',headers={'Authorization':'Bearer '+key})
    with urllib.request.urlopen(req,timeout=15) as r:
        if r.status!=200:raise SystemExit('OmniRoute authentication failed')
    path=ROOT/'data'/'config.local.json';path.parent.mkdir(exist_ok=True)
    cfg=json.loads(path.read_text()) if path.exists() else {}
    cfg.update(ai_provider='omniroute',ai_base_url=args.base_url.rstrip('/'),ai_api_key=key,ai_model=args.model)
    path.write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    print('OmniRoute configured. Key stored only in ignored data/config.local.json; value not printed.')
    print('Model route:',args.model)

if __name__=='__main__':main()
