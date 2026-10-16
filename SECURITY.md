# Security

ClientDesk is a single-user local application. It binds to loopback, checks the Host and request Origin, requires a session token for writes, and does not serve its data directory. Do not expose it through a tunnel or public reverse proxy without adding authentication, HTTPS, rate limits and an authorization model.

Keep OmniRoute credentials in environment variables or `data/config.local.json`. Never commit that file, `.env`, SQLite files, prospect records, logs, backups or local model caches. Browser state and data exports exclude the gateway key. AI prompts are sent to the upstream provider chosen by OmniRoute; keep confidential client information out of prompts unless you have permission and an appropriate provider agreement.

Public-page research accepts only HTTP(S), refuses credentials and unusual ports, blocks private/reserved network addresses, and pins outbound connections to validated public addresses. It bounds response sizes, checks robots.txt and does not bypass browser challenges. It does not perform vulnerability scans.

AI candidate lists can contain stale or invented organizations. Live public-page checks establish reachability and retain evidence; they do not prove identity, company size, a need, consent or buying intent. Review those facts before contacting a prospect. Do not contact records are blocked from outreach generation. The application has no automatic sending capability.

Report a suspected vulnerability privately through the repository owner's GitHub contact or security reporting feature. Do not include live credentials or private prospect data in a public issue. No certification or regulatory compliance claim is made by this project.
