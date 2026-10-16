"""Checks focus on persistent workflow rules and boundary protection."""
import csv, io, json, os, pathlib, tempfile, threading, unittest, urllib.error, urllib.request
from unittest.mock import patch
TASK_TEMP=tempfile.TemporaryDirectory(prefix='clientdesk-test-')
os.environ['CLIENTDESK_DATA']=TASK_TEMP.name
os.environ['CLIENTDESK_PORT']='18787'
import app
import workflows
from integrations import Gateway

class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.init()
        cls.server=app.ThreadingHTTPServer(('127.0.0.1',18787),app.Handler)
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
    def request(self,path,data=None,token=app.TOKEN,origin=None):
        headers={'Content-Type':'application/json','X-ClientDesk-Token':token}
        if origin:headers['Origin']=origin
        req=urllib.request.Request('http://127.0.0.1:18787'+path,data=json.dumps(data).encode() if data is not None else None,headers=headers)
        return urllib.request.urlopen(req)
    def test_duplicate_domain_is_per_company_and_notes_persist(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://www.example.com/a',name='Test'))
        duplicate=app.add_lead(dict(brand='elancebot',url='https://example.com/b'))
        self.assertEqual(lead['id'],duplicate['id'])
        other=app.add_lead(dict(brand='sslsol',url='https://example.com'))
        self.assertNotEqual(other['id'],lead['id'])
        lead.update(stage='Meeting',notes='Confirmed need: profile review',next_date='2026-11-02')
        app.store_lead(lead)
        self.assertEqual(app.lead_by_id(lead['id'])['next_date'],'2026-11-02')
    def test_unknown_offer_and_do_not_contact_block_drafting(self):
        lead=app.add_lead(dict(brand='sslsol',url='https://example.org'))
        with self.assertRaisesRegex(ValueError,'confirm'):app.draft({'id':lead['id']})
        lead['stage']='Do not contact';app.store_lead(lead)
        with self.assertRaisesRegex(ValueError,'Do not contact'):app.draft({'id':lead['id']})
    def test_private_network_and_credential_urls_rejected(self):
        for url in ['http://127.0.0.1','http://169.254.169.254/','http://[::1]','http://localhost/']:
            with self.assertRaises(ValueError):app.public_url(url)
        for url in ['file:///C:/Windows','https://user:password@example.com','https://example.com:9000/']:
            with self.assertRaises(ValueError):app.normalize_url(url)
    def test_origin_and_session_validation(self):
        for kwargs in [dict(token='wrong'),dict(origin='https://untrusted.example')]:
            with self.assertRaises(urllib.error.HTTPError) as e:self.request('/api/lead',{'brand':'elancebot','url':'https://example.net'},**kwargs)
            self.assertEqual(e.exception.code,403)
    def test_database_not_served_and_exports_are_safe(self):
        with self.assertRaises(urllib.error.HTTPError) as e:self.request('/data/clientdesk.sqlite')
        self.assertEqual(e.exception.code,404)
        app.add_lead(dict(brand='elancebot',url='https://example.edu',name='=DANGEROUS()'))
        with self.request('/api/export') as r:rows=list(csv.DictReader(io.StringIO(r.read().decode())))
        self.assertTrue(next(x for x in rows if x['url']=='https://example.edu/')['name'].startswith("'="))
    def test_research_extracts_only_published_contacts_and_evidence(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://public.example'))
        page='<title>Freelancer Academy</title><p>Freelance training and portfolio mentoring. '+('Public business facts. '*8)+'</p><a href="mailto:hello@public.example">Contact</a><a href="/contact">Contact page</a><script>ignore bad script</script>'
        with patch.object(app,'fetch',return_value=(page,'https://public.example/','text/html')):saved=app.research({'id':lead['id']})
        self.assertEqual(saved['public_emails'],['hello@public.example'])
        self.assertEqual(saved['contact_links'],['https://public.example/contact'])
        self.assertNotIn('ignore bad script',saved['sources'][0]['text'])
    def test_browser_draft_preserves_notes_updated_during_generation(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://draft.example'))
        prepared=app.draft({'id':lead['id'],'kind':'brief'})
        self.assertIn('FACTS:',prepared['user'])
        updated=app.lead_by_id(lead['id']);updated['notes']='Meeting rescheduled';app.store_lead(updated)
        app.save_draft({'id':lead['id'],'kind':'brief','text':'A reviewed draft'})
        saved=app.lead_by_id(lead['id'])
        self.assertEqual(saved['notes'],'Meeting rescheduled');self.assertEqual(len(saved['drafts']),1)
    def test_instant_templates_are_explicitly_labeled_and_do_not_invent_prices(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://template.example',name='Potential partner'))
        intro=app.template_draft({'id':lead['id'],'kind':'intro'})
        self.assertEqual(intro['engine'],'Structured local template')
        self.assertIn('[Your name]',intro['text'])
        proposal=app.template_draft({'id':lead['id'],'kind':'proposal'})
        self.assertIn('no commitment made',proposal['text'])

    def test_gateway_key_is_absent_from_state_and_backup(self):
        key='test-secret-never-export-this'
        config=pathlib.Path(TASK_TEMP.name)/'config.local.json'
        config.write_text(json.dumps({'ai_api_key':key}))
        try:
            for endpoint in ['/api/state','/api/backup']:
                with self.request(endpoint) as r:self.assertNotIn(key,r.read().decode())
            self.assertNotIn('api_key',Gateway(TASK_TEMP.name).status())
        finally:config.unlink()

    def test_discovery_preserves_opt_out_and_failed_pages(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://optout.example'))
        lead['stage']='Do not contact';lead['notes']='Preserve this';app.store_lead(lead)
        job=dict(id='optout-job',brand='elancebot',query='test business category in Karachi',count=2,status='queued',lead_ids=[],rejected=[],processed=0)
        workflows.save_job(job)
        candidates=[dict(name='Optout',url=lead['url']),dict(name='Bad',url='https://bad.example')]
        def page(url):
            if 'bad.example' in url:raise ValueError('Robots disallowed')
            return '<p>'+('Public business facts. '*15)+'</p>',url,'text/html'
        with patch.object(workflows,'candidate_list',return_value=(candidates,dict(model='test-model',citations=[]))),patch.object(app,'fetch',side_effect=page):workflows.run_discovery(job['id'])
        result=workflows.get_job(job['id'])
        self.assertEqual(result['status'],'completed');self.assertEqual(result['lead_ids'],[])
        self.assertEqual(len(result['rejected']),2)
        saved=app.lead_by_id(lead['id']);self.assertEqual(saved['stage'],'Do not contact');self.assertEqual(saved['notes'],'Preserve this')

    def test_restore_adds_missing_records_without_overwriting_optout(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://restore.example'))
        original=dict(lead);lead.update(stage='Do not contact',notes='Keep newest');app.store_lead(lead)
        new=dict(original,id='restore-missing',url='https://new-restore.example/')
        result=workflows.restore({'leads':[{'data':json.dumps(original)},{'data':json.dumps(new)}]})
        self.assertEqual(result['added'],1)
        self.assertEqual(app.lead_by_id(lead['id'])['notes'],'Keep newest')
        self.assertEqual(app.lead_by_id(new['id'])['stage'],'Research')
        self.assertTrue(list((pathlib.Path(TASK_TEMP.name)/'backups').glob('*.sqlite')))

    def test_research_does_not_replace_notes_saved_during_fetch(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://race.example'))
        def page(url):
            updated=app.lead_by_id(lead['id']);updated['notes']='Saved during fetch';app.store_lead(updated)
            return '<p>'+('Public business facts. '*15)+'</p>',url,'text/html'
        with patch.object(app,'fetch',side_effect=page):app.research({'id':lead['id']})
        self.assertEqual(app.lead_by_id(lead['id'])['notes'],'Saved during fetch')

    def test_qualification_requires_evidence_and_does_not_invent_a_stage(self):
        lead=app.add_lead(dict(brand='elancebot',url='https://qualify.example'))
        with self.assertRaisesRegex(ValueError,'evidence'):workflows.qualify({'id':lead['id']})
        lead['sources']=[dict(url=lead['url'],text='An academy trains freelancers.')];app.store_lead(lead)
        response=dict(text=json.dumps(dict(summary='Possible fit',hypotheses=['May value profile review'],unknowns=['Budget'])),model='test-model')
        with patch.object(Gateway,'complete',return_value=response):workflows.qualify({'id':lead['id']})
        self.assertEqual(app.lead_by_id(lead['id'])['stage'],'Research')
        self.assertEqual(app.lead_by_id(lead['id'])['assessment']['unknowns'],['Budget'])

if __name__=='__main__':unittest.main(verbosity=2)
