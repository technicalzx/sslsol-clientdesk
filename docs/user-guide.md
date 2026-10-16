# SSLSOL ClientDesk User Guide

ClientDesk helps the SSLSOL owner turn business research into reviewed conversations and a client pipeline. Open the desktop shortcut or visit http://127.0.0.1:8787 while the service is running. Records are stored on this laptop. AI features send selected company facts, prospect evidence and notes through OmniRoute to its configured upstream provider.

## Purpose and business scope

A list of businesses does not establish demand. This workspace saves why a prospect might fit, the public evidence behind that reasoning, questions to validate it and a dated next step. Meetings and revenue depend on the offer, delivery, relationships and follow-through.

SSLSOL services are IT infrastructure, cybersecurity, ERP, AI systems, automation and business solutions for SMBs. Target regions are Pakistan, the Middle East, USA and Europe. Use one business category and one city or country per scan. Region selection is an editable campaign filter, not proof that the business can serve every jurisdiction or language.

## Start and configure

Open the ClientDesk desktop shortcut. The launcher starts the local service and opens the workspace. In Growth playbook, Check OmniRoute makes a live AI request. Stop ClientDesk stops this application; it leaves the separately managed OmniRoute service running. Reopen the shortcut to restart.

In Company brain, select SSLSOL. Check the website, offer, audience and markets. Add verified proof, delivery examples and pricing only when available. Confirm the offer before drafting. The website check records reachability; it is not a security assessment. Restore or confirm public website availability before sending prospects there.

For another installation, install Python 3.11 or newer and run `python launch.py` in the project folder. Core features use the standard library. Run `python scripts/configure_omniroute.py --from-existing` to reuse an existing active OmniRoute endpoint key. The setup reads its local database without changing permissions. Alternatively enter a key privately at the setup prompt. See `.env.example` for environment variable names; environment files are not loaded automatically. Never commit a real key.

---PAGE---

## Discover and review prospects

Open Find prospects. Select a company, market, city or country and category. Choose Use these filters, review the query, and start with three to five candidates. Examples include independent dental clinics in Karachi Pakistan, accounting firms in Dubai UAE, small manufacturers in Austin Texas, or distributors in Berlin Germany.

OmniRoute suggests organizations. The worker checks public websites and saves readable text, a URL and timestamp. The job panel shows saved prospects and rejected candidates with reasons. Jobs persist across navigation. Interrupted jobs need a new scan after restart. Cancel requests take effect between page checks.

A live page check establishes reachability and saves evidence. It does not establish that a model-suggested name, location, size or need is correct. Open the official source and compare its identity with the suggestion. Search execution remains unverified unless the gateway supplies search citations. Company size and buying intent require discovery.

Use Open web search for manual investigation. Add an official website yourself when needed. CSV import accepts `url,name,notes` columns, up to 200 rows. Repeated domains within one company retain the existing record. SSLSOL and Elancebot have separate records.

## Qualify using evidence

Open a prospect and choose Fetch official page. Review its saved text and published contact routes. Only contact links and mailto addresses actually present on the page are extracted. No address is guessed. Verify that a public mailbox is suitable for your purpose.

Choose Assess service fit with AI after saving evidence. Check observations against the sources. Hypotheses are possible needs, not established problems. Use the discovery questions to learn who owns a workflow, how it works now and what would make a pilot useful. Qualification does not automatically change the pipeline stage.

For a clinic, booking or office handoffs might be worth exploring. Do not infer insecure systems, missing backups or patient-data problems from a marketing page. ClientDesk does not scan networks or vulnerabilities.

---PAGE---

## Prepare and record conversations

Save notes before drafting. Use a labeled instant template or one of four OmniRoute drafts: introduction, follow-up, meeting brief or pilot proposal. Review names, factual claims and the proposed next step. Replace signature placeholders. Agree scope, pricing and commitments yourself.

Copying a draft does not send it. Use normal business communication tools after checking the recipient and applicable destination-market requirements. Record actual contact, replies and agreed next steps in Activity history. A saved draft is not proof of sending.

Move stages manually: Research, Qualified, Contacted, Replied, Meeting, Proposal, Won or Lost. Set a follow-up date. Mark opt-outs Do not contact. Drafting is blocked for those records, duplicate imports preserve their stage, and discovery excludes them from saved results.

Save offer sheets, FAQs, verified case studies and meeting notes in Company brain. Questions use the selected profile and up to three notes ranked by keyword overlap. This is a small retrieval workflow, not a complete memory or an independently verified knowledge base. Avoid unnecessary sensitive customer material.

## Review business progress

Use one segment and one service hypothesis per campaign. Record relevant candidates, appropriate conversations, agreed meetings, lessons and pilots. Count observed outcomes, not generated messages. Use CSV export for review. After five to ten real conversations, adjust the segment or offer using needs you actually heard. The workspace supports preparation; it does not deliver the underlying IT or business service.

## Back up and recover

Backup downloads private JSON containing profiles, prospects, knowledge, jobs and activity, excluding the gateway key. CSV export is for review, not full recovery. Keep dated backups outside the project folder.

Restore missing records adds absent prospects and knowledge. It preserves current profiles, existing records and opt-outs, and does not rewind history or jobs. A safety SQLite snapshot is saved under `data/backups` first. Re-enter profiles from the backup if needed.

For full database recovery, stop the app, preserve the current data folder, then restore a known-good SQLite snapshot as `data/clientdesk.sqlite`. Use SQLite backup rather than copying a live database without its WAL files. Restart and verify records. Gateway configuration in `data/config.local.json` is separate and excluded from exports.

---PAGE---

## Troubleshooting and privacy

If the page fails to open, launch the shortcut again and check `data/app.log` or `data/launcher-error.txt`. Resolve port 8787 conflicts without stopping unrelated processes. Keep this single-user service on loopback.

If AI fails, check the existing OmniRoute dashboard at http://127.0.0.1:20128 and its provider connection and quota. Then use Check OmniRoute. The alias `auto/best-free` may select a different upstream model later. HTTP 403 can mean model or key restrictions. Timeouts and rate limits can come from upstream capacity. Instant templates work without AI.

For rejected pages, inspect the reason. Robots restrictions, JavaScript-only sites, access challenges, DNS failures and timeouts are expected. Review an official public page manually and save authorized notes. Do not bypass access controls for research.

Source and sanitized documentation are public at https://github.com/ycgiio/sslsol-clientdesk. Local keys, prospect records, logs, transcript evidence and model downloads are excluded. AI requests share selected context with the upstream provider: local storage does not mean local-only AI computation.

## Suggested first week

Day one: confirm the offer, website availability and one service you can demonstrate. Research three suitable organizations. Day two: verify source facts and contact routes, then prepare concise introductions. Days three and four: conduct appropriate owner-led conversations and record needs, objections and next steps. Day five: review what happened and agree one small pilot only where there is confirmed interest. These are suggested activities, not promised results.
