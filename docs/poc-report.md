# SSLSOL ClientDesk Proof of Concept Report

This report describes the local SSLSOL lead preparation system, verification scope and operating limits for the owner and technical operator. It adapts the interview at https://www.youtube.com/watch?v=v0eruAaxqaQ into a company knowledge and relationship workflow. It does not install Clair Talos, which the interview describes as a private internal system.

## Objective and video analysis

Support SMB client acquisition for SSLSOL IT infrastructure, cybersecurity, ERP, AI systems, automation and business services. Configured target regions are Pakistan, the Middle East, USA and Europe. Each scan focuses on a chosen location and business category. No test establishes market demand or acquired clients.

The interview describes distribution through payroll partners at 2:48 to 3:19, a company brain called Talos at 5:47 to 6:14, and human responsibility for relationships and discovery at 6:46 to 8:30. Missing context is discussed at 11:12 to 11:47. At 26:30 to 27:37, research identifies organizations and people while humans carry relationships forward.

The adaptation combines business facts, public source evidence, relevant notes, draft preparation and a manual pipeline. For SSLSOL, accounting firms, ERP implementers, industry associations and business consultants are distribution hypotheses because they may serve the same SMB audience. Direct prospects and partners should be evaluated in separate focused campaigns.

## Why the workflow is useful

A generic contact list loses context. ClientDesk stores why a prospect was suggested, what a public page says and what still needs validation. The operational question is whether this reduces preparation effort and improves discovery conversations. Commercial results must be measured separately after owner-led outreach.

---PAGE---

## Architecture and data flow

The browser connects to Python on 127.0.0.1:8787. SQLite stores profiles, prospects, knowledge, jobs and activity. A single background worker performs bounded discovery jobs. The key stays server side in ignored configuration or environment variables.

The service calls the existing local OmniRoute endpoint at 127.0.0.1:20128/v1 with an existing active endpoint key. The alias is `auto/best-free`. OmniRoute sends prompts to its configured upstream provider. A live check returned `gemini-3.1-flash-lite`; this is an observed runtime result, not a permanent model or price guarantee.

Discovery converts a focused query into model-suggested candidates, checks public websites and saves source evidence in Research-stage records. Fetching rejects private destinations, checks redirects, connects to a validated public IP, respects robots.txt and limits response size. Failed pages are reported rather than described as verified leads.

Qualification combines the offer, saved page evidence and notes, requesting observations, hypotheses and unknowns separately. Drafting uses the profile, up to two source pages and selected knowledge. Output is rendered as escaped text. The owner reviews it and handles communication.

## Privacy and security boundaries

The API validates Host, Origin and a session token for writes. Assets are served from an explicit allowlist. State and exports exclude gateway credentials. CSV output protects against spreadsheet formula interpretation. Do not contact blocks drafts and survives duplicate imports and additive recovery.

This is a single-user laptop deployment without public hosting or multitenant authentication. Local records need normal laptop and backup protection. AI calls share selected context with the upstream provider. A public repository contains source and sanitized documents, not the private data folder.

---PAGE---

## Verification scope

The reproducible results are recorded in `verification.md`. Thirteen automated checks passed. Acceptance covers workflow rules, public-fetch boundaries, a live gateway completion, discovery, retained source evidence, qualification, saved drafts, company questions, activity, exports and persistence. The desktop interface was inspected in the browser. These checks do not certify third-party business claims.

OmniRoute returned `SSLSOL_GATEWAY_OK` through the configured alias. Search-tool probes did not supply citations. Discovery is therefore described as AI-assisted suggestions with live public-page checks. Requesting a search tool is not represented as proof that search executed.

SSLSOL website availability failed from the laptop during setup. A public DNS query returned a successful DNS response without an A-address answer, which does not establish that the domain is unregistered. The app records its availability result. The owner should verify DNS and hosting before directing prospects there. No DNS or hosting settings were changed.

## Demonstration procedure

Open the shortcut, confirm SSLSOL facts and run Check OmniRoute. Start a three-candidate query. Review saved records, rejections, website identity and source text. Assess one prospect and generate an introduction and pilot outline. Record a demonstration note explicitly stating that no outreach occurred. Download a backup and CSV export.

Repeat a domain to check duplicate handling. In a temporary test database, mark a record Do not contact and verify drafting is blocked. Check restore and private-network boundaries there. Stop and reopen the deployed app to verify persistence. Do not send demonstration outreach to a real prospect.

## Proposed commercial pilot

Review ten suitable organizations and hold five appropriate discovery conversations in one segment. Record preparation time, relevant responses, meetings and pilot interest. Compare the findings with the proposed service afterward. These are suggested pilot targets, not achieved results or conversion promises.

---PAGE---

## Capabilities and limits

Supported: company knowledge, editable regions, bounded discovery, manual and CSV intake, website evidence, published contact routes, service-fit hypotheses, four draft types, company questions, follow-up dates, a manual pipeline, activity, CSV, JSON backup and additive recovery.

Absent: automatic sending, inbox synchronization, paid contact enrichment, authenticated social scraping, challenge bypass, vulnerability scanning, billing and multitenant accounts. Model-suggested identities, locations, size and demand require human verification. The app does not guarantee clients.

Dedicated OmniRoute search services require their own search-provider configuration. A model endpoint key does not create a Brave or Tavily subscription. None was invented. Public Overpass experiments were unreliable and excluded from the delivered active workflow.

A historical browser Qwen utility remains optional source material. Tiny inference worked, but longer generation was unreliable on this laptop. The delivered UI uses OmniRoute. Windows security protections remain enabled.

## Deployment and maintenance

The laptop uses a headless Python launcher and desktop shortcut. Public source: https://github.com/technicalzx/sslsol-clientdesk. CI checks workflow tests, Python compilation and JavaScript syntax. Test backup recovery on a copy, monitor gateway quota, refresh old source evidence and keep queries focused. Broader hosting would require authentication, TLS, access controls and a separate operational design.

## Primary references

Interview: https://www.youtube.com/watch?v=v0eruAaxqaQ

OmniRoute source: https://github.com/diegosouzapw/OmniRoute

Python HTTP server: https://docs.python.org/3/library/http.server.html

SQLite interface: https://docs.python.org/3/library/sqlite3.html

Robot exclusion parser: https://docs.python.org/3/library/urllib.robotparser.html
