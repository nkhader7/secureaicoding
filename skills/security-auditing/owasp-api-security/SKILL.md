---
name: owasp-api-security
description: Audits API implementations against the OWASP API Security Top 10 2023 (API1–API10). Use when reviewing REST, GraphQL, or gRPC APIs for authorization flaws, authentication weaknesses, mass assignment, SSRF, resource abuse, and misconfiguration.
allowed-tools: Bash Read Glob Grep
---

# OWASP API Security Top 10 (2023) Auditor

Systematic security review of API implementations against all ten OWASP API Security risk categories for 2023.

## When to Use

- Security audit of REST, GraphQL, or gRPC API codebases
- Pre-release review of APIs handling user data, payments, or privileged operations
- Code review of authentication, authorization, and input validation logic
- Assessing microservice or third-party API integration security
- Compliance reviews requiring OWASP API alignment

## When NOT to Use

- Runtime traffic analysis (use a WAF or API gateway logs instead)
- Live endpoint penetration testing (use Burp Suite — see `burpsuite-project-parser` skill)
- General web application review without an API component (use OWASP Web Top 10)
- Smart contract APIs (use `building-secure-contracts` skill)

## The Ten Risk Categories

### API1:2023 — Broken Object Level Authorization (BOLA / IDOR)

**Root cause**: Endpoints accept user-supplied object IDs without verifying the requester owns or has permission to access that object.

**Exploitability**: Easy — change a numeric or UUID parameter; the server returns another user's data.

**Detection targets**:
- Route handlers that accept `:id`, `{id}`, `userId`, `documentId`, etc. as path/query parameters
- Absence of an ownership or permission check between ID extraction and the database query
- GraphQL resolvers querying by ID without caller context validation

**Red flags**:
```python
# VULNERABLE: no ownership check
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    return db.query(Invoice).get(invoice_id)  # returns any user's invoice

# SAFE: ownership enforced
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id, Invoice.owner_id == current_user.id
    ).first()
    if not invoice:
        raise HTTPException(403)
    return invoice
```

**References**: CWE-285, CWE-639 | [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

---

### API2:2023 — Broken Authentication

**Root cause**: Authentication mechanisms accept forged, expired, or unsigned tokens; lack brute-force protection; or allow weak credential policies.

**Exploitability**: Easy — tools for credential stuffing and JWT attacks are widely available.

**Detection targets**:
- JWT decoded without signature verification (`verify_signature: False`, algorithm `"none"`)
- Missing `algorithms` allowlist in `jwt.decode` — allows algorithm confusion
- Login and password-reset endpoints without rate limiting
- GraphQL mutation batching used to bypass per-request rate limits
- Hardcoded or predictable JWT secrets (`"secret"`, `"changeme"`)

**Red flags**:
```python
# VULNERABLE: signature bypassed
payload = jwt.decode(token, options={"verify_signature": False})

# VULNERABLE: "none" algorithm accepted
payload = jwt.decode(token, key, algorithms=["HS256", "none"])
```

**References**: CWE-287, CWE-307, CWE-798

---

### API3:2023 — Broken Object Property Level Authorization

**Root cause**: Endpoints expose sensitive object properties to readers, or allow callers to write to properties they should not control — combining Excessive Data Exposure and Mass Assignment.

**Exploitability**: Easy — inspect responses for unexposed fields; replay write requests with extra properties.

**Detection targets**:
- Serializers returning whole model objects without an explicit field allowlist
- Mass assignment: binding the entire request body to a model
- GraphQL responses returning internal fields (`isAdmin`, `blocked`, `internalScore`)
- Missing schema-based response validation

**Red flags**:
```javascript
// VULNERABLE: entire body written to model — attacker can set isAdmin=true
User.findByIdAndUpdate(userId, req.body);

// SAFE: explicit field allowlist
const { name, email } = req.body;
User.findByIdAndUpdate(userId, { name, email });
```

```python
# VULNERABLE: returns every column, including password_hash, is_admin
return jsonify(user.__dict__)

# SAFE: cherry-pick fields
return jsonify({ "id": user.id, "email": user.email, "name": user.name })
```

**References**: CWE-213, CWE-915 | [Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)

---

### API4:2023 — Unrestricted Resource Consumption

**Root cause**: APIs impose no limits on request rate, payload size, query depth, or records returned, enabling DoS, memory exhaustion, and financial abuse via third-party cost amplification.

**Exploitability**: Easy — send many requests or one very large request.

**Detection targets**:
- Database queries without a `LIMIT` / `take` / `TOP` clause
- File upload handlers with no size validation
- Pagination endpoints with no enforced maximum `page_size`
- GraphQL with no query depth or complexity limit
- Third-party API calls (SMS, email, AI) triggered per user action without spend caps

**Red flags**:
```python
# VULNERABLE: returns every matching row
results = db.query(User).filter_by(active=True).all()

# VULNERABLE: file size unchecked
file_data = request.files['upload'].read()

# SAFE
MAX_PAGE_SIZE = 100
page_size = min(int(request.args.get("page_size", 20)), MAX_PAGE_SIZE)
results = db.query(User).filter_by(active=True).limit(page_size).all()
```

**References**: CWE-770, CWE-400

---

### API5:2023 — Broken Function Level Authorization (BFLA)

**Root cause**: Privileged API functions (admin operations, bulk exports, delete-all) are accessible to lower-privileged callers because HTTP-verb or role checks are absent.

**Exploitability**: Easy — guess admin endpoint paths; change HTTP verb from `GET` to `DELETE`.

**Detection targets**:
- Routes under `/admin/`, `/internal/`, `/management/` without an explicit role guard
- `DELETE`, `PUT`, or `PATCH` handlers that lack authorization checks even when the corresponding `GET` is protected
- Functions mutating other users' data accessible to any authenticated user
- Missing deny-by-default on administrative abstract controllers

**Red flags**:
```python
# VULNERABLE: any authenticated user can delete any account
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    db.query(User).filter(User.id == user_id).delete()  # no admin check

# SAFE
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, _=Depends(require_role("admin"))):
    ...
```

**References**: CWE-285

---

### API6:2023 — Unrestricted Access to Sensitive Business Flows

**Root cause**: Business-critical flows (purchase, reservation, referral credit) have no protection against automated or programmatic abuse, allowing scalping, inventory squatting, or reward farming.

**Exploitability**: Easy with scripting — no cryptography or credentials to break.

**Detection targets**:
- Purchase / checkout / booking endpoints without device fingerprinting or CAPTCHA
- Referral or reward endpoints callable in unlimited loops per account
- Ticket / seat / inventory reservation with no per-user hold limits
- Bulk operations (add-to-cart, vote, follow) with no velocity check beyond global rate limits

**Investigation approach**: Map the business model first. Identify flows where automated abuse causes economic harm or unfair advantage. Verify that protections are on those specific high-value flows — global rate limits alone are insufficient.

**References**: CWE-770, CWE-799

---

### API7:2023 — Server-Side Request Forgery (SSRF)

**Root cause**: Endpoints accept user-supplied URLs and issue outbound HTTP requests without validating the destination, letting attackers reach internal services, cloud metadata endpoints, or other private hosts.

**Exploitability**: Easy — supply `http://169.254.169.254/` (AWS metadata) or `http://localhost:6379` (Redis).

**Detection targets**:
- HTTP fetch functions called with URL values from request body, query params, or headers
- Webhook registration that stores and later calls user-provided URLs
- File import/export that fetches from user-provided remote paths
- Outbound HTTP clients with redirect-following enabled and no destination allowlist

**Red flags**:
```python
# VULNERABLE: user controls the URL
url = request.json.get("callback_url")
response = requests.get(url)  # can reach 169.254.169.254

# SAFE: allowlist enforced
ALLOWED_HOSTS = {"api.partner.com", "cdn.myapp.com"}
parsed = urlparse(url)
if parsed.hostname not in ALLOWED_HOSTS or parsed.scheme != "https":
    raise ValueError("Disallowed URL")
response = requests.get(url, allow_redirects=False)
```

**References**: CWE-918 | [SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

---

### API8:2023 — Security Misconfiguration

**Root cause**: Default or permissive settings across any layer of the API stack expose unnecessary attack surface — CORS wildcards, debug modes, verbose error responses, missing TLS, unpinned dependencies.

**Exploitability**: Easy — misconfigurations are discoverable with automated tools.

**Detection targets**:
- `DEBUG = True` or equivalent active in production config files
- `Access-Control-Allow-Origin: *` on authenticated API endpoints
- Error handlers returning stack traces or exception details to clients
- HTTP (not HTTPS) for internal service communication
- Unnecessary HTTP verbs enabled (`TRACE`)
- Missing `Cache-Control: no-store` on sensitive API responses
- JNDI / placeholder expansion in logging libraries (log4j-style)

**Red flags**:
```python
app.config['DEBUG'] = True                          # full stack trace in every 500
CORS(app, resources={r"/*": {"origins": "*"}})      # any origin accepted
```

**References**: CWE-16, CWE-209, CWE-319, CWE-942

---

### API9:2023 — Improper Inventory Management

**Root cause**: Outdated or shadow API versions remain running without the security controls of the current version; sensitive data flows to third parties are undocumented and unmonitored.

**Exploitability**: Easy — find old version prefixes via Google Dorking or DNS enumeration; they often skip rate limiting, auth, or input validation added in later versions.

**Detection targets**:
- Multiple API version prefixes in the same codebase (`/v1/`, `/v2/`, `/beta/`, `/legacy/`) where older versions lack security middleware parity
- Deprecated endpoints not returning `410 Gone` or redirect to current version
- No OpenAPI/Swagger documentation generation in CI pipeline
- Third-party integrations with undocumented data flows

**Investigation approach**: Enumerate all route prefixes. For each older version, diff the security middleware stack against the latest. Missing rate limiting, auth, or validation in an old version = finding.

**References**: CWE-1059

---

### API10:2023 — Unsafe Consumption of APIs

**Root cause**: Applications trust data from third-party APIs without applying the same validation used for user input, enabling injection attacks through a compromised or malicious upstream service.

**Exploitability**: Moderate — requires upstream service compromise or a malicious provider.

**Detection targets**:
- Third-party API responses used directly in SQL queries, HTML rendering, OS commands, or file paths
- Outbound HTTP calls using plain HTTP instead of HTTPS
- Missing timeout configuration on third-party HTTP clients
- `allow_redirects=True` on outbound calls to third parties
- No input schema validation on data received from external services

**Red flags**:
```python
# VULNERABLE: upstream data injected into SQL
data = requests.get("https://partner.api/users").json()
db.execute(f"SELECT * FROM users WHERE email = '{data['email']}'")

# SAFE: validate before using
email = data.get("email", "")
if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
    raise ValueError("Invalid email from upstream API")
db.execute("SELECT * FROM users WHERE email = %s", (email,))
```

**References**: CWE-20, CWE-346

---

## Audit Workflow

**Phase 1: Scope & Map** (use `audit-context-building` skill)
- Identify all API entry points: REST routes, GraphQL schema, gRPC proto files
- Document authentication mechanism and user/role hierarchy
- List all outbound HTTP calls and third-party integrations

**Phase 2: Authorization Sweep** (API1, API3, API5)
- Enumerate every endpoint accepting an object ID or performing state change
- For each: confirm ownership check (API1), field allowlist on reads/writes (API3), role guard on privileged verbs (API5)
- Prioritize write operations and cross-user data access patterns

**Phase 3: Authentication & Token Review** (API2)
- Locate all JWT decode/verify call sites — check algorithm allowlist, expiry enforcement, and signature verification
- Find login, password-reset, and account-change endpoints — verify rate limiting and re-authentication
- Review token storage, transport, and comparison patterns

**Phase 4: Injection & Misconfiguration Scan** (API7, API8, API10)
- Run `reference/rules.yaml` patterns against source to surface SSRF triggers and misconfiguration
- Verify CORS policy, debug flags, TLS enforcement, and error handler output
- Audit every outbound HTTP call for URL validation and data sanitization on the response

**Phase 5: Resource & Business Flow Review** (API4, API6)
- Check all paginated endpoints for enforced `max_page_size` and query limits
- Identify business-critical flows; confirm bot/automation protection on each high-value flow specifically

**Phase 6: Inventory & Third-Party Audit** (API9, API10)
- Enumerate all route prefixes; compare security middleware across versions
- List all outbound HTTP clients; verify TLS, timeouts, redirect policy, and response validation

**Phase 7: Report**
- Use `_shared/report-template.md` for findings
- Tag each finding with API category (API1–API10), CWE, and severity
- Include evidence: file path, line number, and a concrete exploit scenario

## Severity Mapping

| Category | Default Severity | Rationale |
|---|---|---|
| API1 BOLA | Critical | Direct unauthorized data access across users |
| API2 Broken Auth | Critical | Account takeover vector |
| API3 Property AuthZ | High | Data exposure or privilege escalation |
| API4 Resource Consumption | High | DoS and financial damage via cost amplification |
| API5 BFLA | Critical | Unauthorized access to admin/privileged functions |
| API6 Business Flow | Medium–High | Business-specific; economic harm or fraud |
| API7 SSRF | High | Internal network access, credential theft via metadata |
| API8 Misconfiguration | Medium–High | Broad attack surface; varies by specific issue |
| API9 Inventory | Medium | Exploitation of shadow APIs with weaker controls |
| API10 Unsafe Consumption | High | Injection via trusted upstream; hard to detect in prod |

## Reference Files

- [attack-scenarios.md](references/attack-scenarios.md) — Concrete attack scenarios for all 10 categories
- [checklist.md](references/checklist.md) — Per-endpoint audit checklist

## Rationalizations to Reject

- **"The object ID is a UUID so BOLA isn't exploitable"** → UUIDs reduce enumeration but do not enforce authorization; a leaked UUID is fully exploitable
- **"Rate limiting is on the load balancer"** → Verify it applies to every API version including beta/staging hosts; shadow hosts often bypass it
- **"We validate input before using third-party data"** → Show the validation code; unsupported claims are not evidence
- **"The admin endpoint URL isn't in our docs"** → Security through obscurity is not authorization
- **"Third-party data is safe because it comes over HTTPS"** → TLS proves transport integrity, not content safety; validate anyway
- **"Debug mode is only on in dev"** → Check every environment config file and deployment manifest; misconfiguration routinely bleeds into staging
- **"CORS wildcard is fine because auth uses tokens"** → Token-bearing requests from any origin become exploitable if XSS exists anywhere on the page
