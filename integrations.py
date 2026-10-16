"""Server-side OmniRoute client. Secrets never enter the browser or exports."""
import json, os, pathlib, re, threading, time, urllib.error, urllib.request

AI_LOCK = threading.BoundedSemaphore(1)

class GatewayError(ValueError):
    pass

class Gateway:
    def __init__(self, data_dir):
        self.data_dir=pathlib.Path(data_dir)

    def config(self):
        path=self.data_dir/'config.local.json'
        conf=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        return {
            'base_url':os.environ.get('OMNIROUTE_BASE_URL',conf.get('ai_base_url','http://127.0.0.1:20128/v1')).rstrip('/'),
            'api_key':os.environ.get('OMNIROUTE_API_KEY',conf.get('ai_api_key','')),
            'model':os.environ.get('OMNIROUTE_MODEL',conf.get('ai_model','auto/best-free')),
        }

    def status(self):
        c=self.config()
        return dict(provider='OmniRoute',configured=bool(c['api_key']),base_url=c['base_url'],model=c['model'],
                    note='Prompts go through OmniRoute to its selected upstream model. Quotas and provider terms apply.')

    def complete(self,system,user,max_tokens=900,search=False):
        c=self.config()
        if not c['api_key']:raise GatewayError('Configure OmniRoute with scripts/configure_omniroute.py or environment variables.')
        if not AI_LOCK.acquire(timeout=2):raise GatewayError('Another AI task is running. Try again when it finishes.')
        start=time.monotonic()
        try:
            payload=dict(model=c['model'],messages=[dict(role='system',content=system),dict(role='user',content=user)],
                         max_tokens=max_tokens,temperature=.2,stream=False)
            if search:
                payload['tools']=[{'type':'function','function':{'name':'google_search','description':'Search public business websites','parameters':{'type':'object','properties':{}}}}]
            req=urllib.request.Request(c['base_url']+'/chat/completions',data=json.dumps(payload).encode(),
                headers={'Content-Type':'application/json','Authorization':'Bearer '+c['api_key'],'User-Agent':'SSLSOL-ClientDesk/2.0'})
            try:
                with urllib.request.urlopen(req,timeout=55) as r:result=json.loads(r.read(2000000))
            except urllib.error.HTTPError as e:
                # Provider error bodies can echo credentials. Return a bounded, secret-free message.
                raise GatewayError(f'OmniRoute returned HTTP {e.code}. Check its dashboard, model access and provider quota.') from None
            except (OSError,ValueError):
                raise GatewayError('OmniRoute is unavailable or timed out. Start OmniRoute and check its dashboard.') from None
            message=result.get('choices',[{}])[0].get('message',{})
            text=message.get('content') or ''
            if not isinstance(text,str) or not text.strip():raise GatewayError('The model returned no usable text. Try again or use an instant template.')
            return dict(text=re.sub(r'<think>.*?</think>','',text,flags=re.S).strip(),
                        model=result.get('model',c['model']),provider='OmniRoute',seconds=round(time.monotonic()-start,2),
                        truncated=result['choices'][0].get('finish_reason')=='length',
                        citations=message.get('citations',[]),search_requested=search)
        finally:AI_LOCK.release()

def json_result(text):
    text=re.sub(r'^```(?:json)?\s*|\s*```$','',text.strip(),flags=re.I)
    try:return json.loads(text)
    except ValueError:
        # Accept prose surrounding a JSON object, without evaluating code.
        start=text.find('{');end=text.rfind('}')
        if start>=0 and end>start:
            try:return json.loads(text[start:end+1])
            except ValueError:pass
    raise GatewayError('The model did not return valid JSON. No generated contacts or candidates were imported.')
