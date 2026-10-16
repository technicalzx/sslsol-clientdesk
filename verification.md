# Deployment verification

Observed on 16 October 2026, Asia/Karachi. Private prospect records and raw integration outputs remain outside this repository.

## Automated checks

`python -m unittest -v`: **13 tests passed**, in a separate temporary database. Tests cover per-company duplicate domains, note and follow-up persistence, unconfirmed offers, opt-out draft blocking, public-network URL boundaries, request Origin and session tokens, protected database paths, CSV formula protection, published-contact extraction, concurrent note preservation during research and drafting, secret exclusion from state/backup, rejected discovery candidates, additive restore and evidence-required qualification without automatic stage changes.

Python compilation and `node --check web/app.js` passed. CI runs these same checks without real provider credentials. Temporary recovery snapshots closed cleanly after fixing a Windows file-handle issue.

## Live integration and workflow

- `/health` returned HTTP 200 with `app: clientdesk` and `status: ok`. Listener confirmed on **127.0.0.1:8787** only.
- Existing OmniRoute endpoint key reused privately; no scopes or provider configuration changed. `auto/best-free` returned `SSLSOL_GATEWAY_OK`, actual model `gemini-3.1-flash-lite`, in 4.31 seconds on the recorded check.
- First three-candidate Karachi clinic scan saved two source-backed candidates and rejected a website declaring `utf8mb4`. A safe UTF-8 fallback fixed the unsupported encoding. A repeat scan initiated in the browser saved three candidates with zero rejections, while preserving existing domains.
- Public source text, URL, timestamps and published contact routes were retained. Business size and buying intent remained unverified. Search-tool probes supplied no citations, so search execution is explicitly unverified.
- Live service-fit assessment separated observations, hypotheses, questions and unknowns. The prospect remained at Research.
- All four OmniRoute draft types saved with actual model names and review labels. Recorded introduction and pilot generation times were 2.38 and 2.81 seconds; a meeting brief took 12.8 seconds. The company-brain answer completed in 1.59 seconds. These are individual observations, not performance guarantees.
- Demonstration activity explicitly recorded that no outreach occurred. No external messages were sent and no client was marked won.
- JSON backup and CSV export returned nonempty payloads. Guide and POC PDF routes returned HTTP 200 and `application/pdf`.
- Browser inspection confirmed the SSLSOL default pipeline, regional discovery controls, saved research, assessment, drafts, activity and website check. The service was stopped through the UI and restarted through the headless launcher; saved evidence and drafts persisted.
- Two four-page PDFs were rendered with bundled Poppler and visually inspected page by page. Markdown source is also supplied. An optional DOCX draft was not delivered because the environment lacked LibreOffice for required render verification.

## Website availability

The app's SSLSOL availability check failed DNS resolution. Google public DNS queries for `sslsol.com` returned status 0 with no A, AAAA or CNAME answer. This does not establish that the domain is unregistered. The owner should verify domain DNS and hosting before directing prospects there. No DNS settings were modified.

## Deployment scope

The configured laptop has a ClientDesk desktop shortcut and existing virtual environment. OmniRoute remains separately managed at its existing local endpoint. Public source, sanitized documentation, MIT license, security guidance and CI configuration are included. Credentials, prospect data, local backups, logs, transcript evidence and runtime downloads are excluded.

Fresh checkouts have no prospect seed dataset and require the owner to confirm company facts. AI availability depends on the configured upstream provider and quota. This is a single-user local research and preparation workflow; it does not verify demand or guarantee client acquisition.
