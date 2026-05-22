# Per-Endpoint Audit Checklist — OWASP API Security Top 10 2023

Use this checklist for every API endpoint under review. Mark each item ✅ (passes), ❌ (fails — finding), or N/A.

---

## Pre-Audit: Scope Setup

- [ ] All API entry points identified (REST routes, GraphQL schema, gRPC .proto files)
- [ ] Authentication mechanism documented (JWT, session cookie, API key, OAuth2)
- [ ] User/role hierarchy mapped (anonymous, user, admin, service-to-service)
- [ ] Third-party integrations and outbound HTTP calls listed
- [ ] All API version prefixes enumerated (`/v1/`, `/v2/`, `/beta/`, `/legacy/`)

---

## API1 — Broken Object Level Authorization (BOLA)

For every endpoint that accepts an object ID:

- [ ] The endpoint retrieves only objects owned by or explicitly shared with the authenticated caller
- [ ] Ownership/permission check is performed AFTER authentication and BEFORE the database query
- [ ] The check uses server-side session/token context — not a client-supplied user ID
- [ ] UUIDs are used as record IDs (reduces enumeration; does not replace authorization)
- [ ] Tests exist that verify one user cannot access another user's objects

**Key question**: Can I change the ID in the request and receive another user's data?

---

## API2 — Broken Authentication

- [ ] JWT signature verification is always enabled (no `verify_signature: False`)
- [ ] Algorithm is explicitly allowlisted — `"none"` is not in the list
- [ ] JWT expiry (`exp`) is validated on every request
- [ ] Login endpoint: rate limited and/or locked after N failures
- [ ] Password reset endpoint: same security rigor as login
- [ ] Sensitive actions (email change, password change, payment) require re-authentication
- [ ] JWT secrets are ≥256 bits, stored in a secrets manager, and rotated on compromise
- [ ] GraphQL batching cannot be used to bypass per-request rate limits

**Key question**: Can I skip, forge, or replay authentication to access protected endpoints?

---

## API3 — Broken Object Property Level Authorization

For every endpoint that returns or accepts an object:

**Reads (Excessive Data Exposure)**:
- [ ] Response serializer uses an explicit field allowlist (not `.to_json()`, `.__dict__`, `.toObject()`)
- [ ] Sensitive fields (`password_hash`, `is_admin`, `internal_score`, `blocked`) are excluded from all responses
- [ ] Response schema is defined and enforced (e.g., OpenAPI `response` schema)

**Writes (Mass Assignment)**:
- [ ] Writable fields are explicitly allowlisted in the controller or serializer
- [ ] `req.body`, `request.data`, or `params` are never passed directly to `.update()` / `.assign()` without filtering
- [ ] Fields like `role`, `is_admin`, `credit_balance`, `blocked` cannot be set by the caller via normal write endpoints

**Key question**: Can I read a field I shouldn't see, or write a field I shouldn't control?

---

## API4 — Unrestricted Resource Consumption

- [ ] All paginated endpoints enforce a maximum `page_size` (e.g., `min(requested, MAX)`)
- [ ] All database queries have a `LIMIT` / `take` clause
- [ ] File upload endpoints validate file size before processing
- [ ] GraphQL has query depth and complexity limits configured
- [ ] Third-party API calls that incur cost (SMS, email, AI inference) are rate-limited per user
- [ ] Execution timeouts are set on long-running operations
- [ ] Containerized services have memory and CPU limits set

**Key question**: Can I trigger resource exhaustion or unexpectedly large costs with a single or repeated request?

---

## API5 — Broken Function Level Authorization (BFLA)

- [ ] Every admin or privileged endpoint enforces a role/group check before execution
- [ ] Administrative endpoints are not accessible to regular authenticated users regardless of URL path
- [ ] All HTTP verbs (GET, POST, PUT, PATCH, DELETE) are individually authorized — not just the "primary" verb
- [ ] Deny-by-default: access is explicitly granted per role, not implicitly inherited
- [ ] Administrative abstract controllers are used and inherited, not copy-pasted per controller

**Key question**: Can I access an admin function by changing the HTTP method, guessing the URL, or escalating from a regular user account?

---

## API6 — Unrestricted Access to Sensitive Business Flows

Identify high-value business flows (purchase, reservation, referral, vote):

- [ ] Each high-value flow has per-user velocity limits beyond global rate limiting
- [ ] Purchase / checkout flows have fraud/abuse detection or CAPTCHA
- [ ] Referral and reward endpoints validate account uniqueness (email, device, payment method)
- [ ] Reservation flows enforce per-user hold limits and expiry
- [ ] B2B / developer API endpoints that expose business flows have separate, stricter controls

**Key question**: Can I automate this flow to gain unfair economic advantage or exhaust inventory/capacity?

---

## API7 — Server-Side Request Forgery (SSRF)

For every endpoint that issues outbound HTTP requests:

- [ ] Destination URL is validated against an explicit allowlist of permitted hosts and schemes
- [ ] `allow_redirects=False` (or equivalent) is set on the HTTP client
- [ ] No URL from request body, query string, or headers is fetched without validation
- [ ] Cloud metadata endpoints (169.254.169.254, fd00:ec2::254) are explicitly blocked
- [ ] Webhook registration validates and stores only pre-approved callback URLs
- [ ] Import/export features that fetch remote files validate the source URL

**Key question**: Can I make the server issue an HTTP request to an internal address or cloud metadata endpoint?

---

## API8 — Security Misconfiguration

- [ ] `DEBUG = False` in all non-development environments
- [ ] CORS policy uses an explicit origin allowlist — no wildcard on authenticated endpoints
- [ ] Error handlers return generic messages to clients; full details logged server-side only
- [ ] All communication uses HTTPS/TLS — no plaintext HTTP between services
- [ ] Only required HTTP verbs are enabled on each endpoint; `TRACE` is disabled
- [ ] `Cache-Control: no-store` on sensitive API responses
- [ ] Security headers present: `Content-Type`, `X-Content-Type-Options`, `Strict-Transport-Security`
- [ ] No unnecessary features enabled (GraphQL introspection off in production, stack trace middleware removed)

**Key question**: Does any layer of the API stack have a default or permissive configuration that an attacker can exploit?

---

## API9 — Improper Inventory Management

- [ ] All API versions and hosts are documented (environment, access scope, version)
- [ ] Deprecated API versions return `410 Gone` or redirect to the current version
- [ ] All old API versions have the same security middleware as the current version (auth, rate limiting, validation)
- [ ] API documentation is auto-generated from code (OpenAPI) and kept up to date in CI
- [ ] Non-production environments (beta, staging, test) do not use production data
- [ ] Third-party data flows are documented: what data, which service, business justification

**Key question**: Are there shadow or deprecated API hosts with weaker security controls than the current production version?

---

## API10 — Unsafe Consumption of APIs

For every outbound call to a third-party service:

- [ ] Third-party API response data is validated against a schema before use
- [ ] External data is sanitized before being used in SQL queries, HTML rendering, or OS commands
- [ ] All outbound calls use HTTPS — no plain HTTP to external services
- [ ] Timeout is configured on every outbound HTTP client call (connect + read timeout)
- [ ] Redirect following is disabled or redirects are validated against an allowlist
- [ ] Third-party API contracts (schema, error formats) are documented and monitored for changes

**Key question**: If the third-party API returns malicious data, does our application execute or store it unsafely?

---

## Severity Reference

| Finding | Severity |
|---|---|
| BOLA — unauthorized read/write of another user's object | Critical |
| Auth bypass — signature disabled, algorithm confusion | Critical |
| BFLA — admin function accessible without role check | Critical |
| Mass assignment — caller can set privileged fields | High |
| SSRF — user-controlled URL fetched without allowlist | High |
| Excessive data exposure — sensitive fields in response | High |
| Resource consumption — no pagination / rate limit | High |
| CORS wildcard on authenticated endpoint | High |
| Unsafe consumption — third-party data in SQL/HTML | High |
| Debug mode enabled in production | High |
| Stack trace in error response | Medium |
| Missing HTTPS for internal services | Medium |
| Redirect following without allowlist | Medium |
| No timeout on outbound HTTP client | Medium |
| Deprecated API version without security parity | Medium |
| Business flow without automation protection | Medium–High |
