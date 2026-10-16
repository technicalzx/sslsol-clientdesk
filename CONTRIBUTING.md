# Contributing

Use Python 3.12 or newer. Core execution uses the standard library. Run `python -m unittest discover -v`, `python -m py_compile app.py integrations.py workflows.py launch.py` and `node --check web/app.js` before opening a pull request.

Use additive database changes and preserve existing profiles, notes, drafts and opt-outs. Add a mocked test for new external API behavior and keep live tests explicit and optional. Never add real credentials, private leads, backups or scraped documents to fixtures. Label generated suggestions and hypotheses clearly.

Please describe the user-visible problem, the resulting behavior and your validation evidence. Keep changes focused and document any new network destination, quota, license or data-retention behavior.
