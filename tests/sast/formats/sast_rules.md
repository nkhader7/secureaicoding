# SAST Rules — Markdown Format

> **Format note**: Markdown is human-readable documentation, not a machine-readable rule format.
> This file describes the same 5 rules as the YAML/TOML/JSON files but in prose form.
> An automated scanner cannot extract regex patterns from this file without a custom parser.
> Detection accuracy for automated scanning: **0%** — this format requires a human reviewer.

---

## Rule API2-001: JWT Signature Verification Disabled

**Category**: API2:2023 Broken Authentication  
**Severity**: Critical  
**File types**: `.py`, `.js`, `.ts`, `.go`, `.java`, `.cs`, `.rb`

### What to Look For

Look for any call to `jwt.decode()` (Python), `jwt.verify()` (Node.js), or equivalent token
decoding function where signature verification has been explicitly disabled. Common indicators:

- `verify_signature=False` or `options={"verify_signature": False}` in Python PyJWT
- `IgnoreSignatureValidation = true` in C# / Java JWT libraries
- `ignoreExpiration: true` in Node.js `jsonwebtoken`
- `require_exp = False` in Python PyJWT

### Why It's Dangerous

Without signature verification the server accepts any token, including ones the attacker
crafted locally. The entire authentication trust model collapses.

### Remediation

Always verify JWT signatures. Use an explicit algorithm allowlist: `algorithms=["HS256"]`.
Never accept the `"none"` algorithm.

---

## Rule API2-002: JWT 'none' Algorithm Accepted

**Category**: API2:2023 Broken Authentication  
**Severity**: Critical  
**File types**: `.py`, `.js`, `.ts`, `.go`, `.java`, `.cs`, `.rb`

### What to Look For

Find JWT decode calls where the `algorithms` list includes the string `"none"`. Example:

```python
# VULNERABLE
jwt.decode(token, key, algorithms=["HS256", "none"])
```

### Why It's Dangerous

The `none` algorithm tells the library to skip signature validation. An attacker can strip
the signature from any valid token, set `alg: none`, and the library will accept it.

### Remediation

Remove `"none"` from the algorithm list. Never mix symmetric (`HS256`) and asymmetric
(`RS256`) algorithms in the same allowlist.

---

## Rule API3-001: Mass Assignment — req.body Bound to Model

**Category**: API3:2023 Broken Object Property Level Authorization  
**Severity**: High  
**File types**: `.js`, `.mjs`, `.ts`, `.py`, `.rb`, `.php`, `.java`

### What to Look For

Find patterns where the entire HTTP request body is bound directly to a model object:

```javascript
// VULNERABLE
Object.assign(user, req.body);
User.findByIdAndUpdate(userId, req.body);
```

```python
# VULNERABLE
user.update_attributes(params)
```

### Why It's Dangerous

Callers can set internal fields like `isAdmin`, `role`, or `creditBalance` by including them
in the request body. No code change required — just a crafted HTTP request.

### Remediation

Extract only the fields callers are permitted to set. Use serializer schemas with explicit
`fields` or `read_only_fields` declarations.

---

## Rule API7-001: SSRF — User-Controlled URL Fetched

**Category**: API7:2023 Server Side Request Forgery  
**Severity**: High  
**File types**: `.py`, `.js`, `.ts`, `.go`, `.rb`, `.php`, `.java`

### What to Look For

Find HTTP fetch calls where the URL comes from request parameters, body, or headers:

```python
# VULNERABLE
url = request.json.get('callback_url')
response = requests.get(url)
```

```javascript
// VULNERABLE
const response = await axios.get(req.body.webhookUrl);
```

### Why It's Dangerous

Attackers can reach internal services, cloud metadata endpoints (`169.254.169.254`), or
other hosts invisible to external networks. May expose IAM credentials or internal APIs.

### Remediation

Validate the URL against an explicit allowlist of permitted hosts and schemes before
issuing the request. Disable redirect following.

---

## Rule API8-001: Debug Mode Hardcoded True

**Category**: API8:2023 Security Misconfiguration  
**Severity**: High  
**File types**: `.py`, `.js`, `.ts`, `.rb`, `.php`, `.yaml`, `.yml`, `.env`, `.cfg`

### What to Look For

Find configuration files or application code with debug mode hardcoded to `True`:

```python
# VULNERABLE
DEBUG = True
app.run(debug=True)
```

```yaml
# VULNERABLE
debug: true
```

### Why It's Dangerous

Debug mode typically causes the framework to return full stack traces in HTTP 500 responses,
exposes interactive debuggers (Werkzeug debugger), and disables security hardening.

### Remediation

Read the debug flag from an environment variable and default to `False`:

```python
# SAFE
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
```
