---
name: firebase-apk-scanner
description: Scans Android APKs for Firebase misconfigurations and security vulnerabilities. For authorized security testing only.
allowed-tools: Bash Read Write Glob Grep
---

# Firebase APK Scanner

**For authorized security research only.** Do not scan apps without explicit permission or test production Firebase projects without written consent.

## When to Use

- Authorized penetration testing of Android applications
- Security assessment of apps that use Firebase backend
- Validating Firebase security rules before release
- Bug bounty research with explicit scope permission

## What It Tests

| Category | Tests |
|----------|-------|
| Authentication | Open signup, anonymous auth capabilities |
| Realtime Database | Access control rules, unauthenticated read/write |
| Firestore | Document and collection exposure |
| Cloud Storage | Bucket permissions, public access |
| Cloud Functions | Accessibility, authentication requirements |
| Remote Config | Data exposure, parameter leakage |

## Severity Classification

| Severity | Example |
|----------|---------|
| CRITICAL | Unauthenticated write to Realtime Database |
| HIGH | Authenticated user can read other users' data |
| MEDIUM | Anonymous authentication enabled (depends on use) |
| LOW | Remote Config parameters visible without auth |

## Workflow

1. **Validate** the APK input and confirm authorization scope
2. **Execute** the scanner script to decompile and extract Firebase configs
3. **Present** findings with severity classification
4. **Provide** specific remediation guidance per finding
5. **Clean up** any test data created during testing

## Common Vulnerabilities

**Open Realtime Database** — `.read: true` or `.write: true` at root:
```json
{
  "rules": {
    ".read": true,    // Anyone can read all data
    ".write": true    // Anyone can write/delete all data
  }
}
```

**Insecure Firestore Rules**:
```javascript
// VULNERABLE: Any authenticated user can access any document
match /{document=**} {
  allow read, write: if request.auth != null;
}
```

**Unsafe Anonymous Auth usage**:
- Anonymous auth enabled AND sensitive operations allowed for anonymous users

## Manual Testing Fallback

If automated scanner fails:

```bash
# Extract Firebase config from APK
apktool d app.apk -o decompiled/
grep -r "google-services.json\|firebase" decompiled/ --include="*.json"

# Test Realtime Database access
curl "https://<project>.firebaseio.com/.json"

# Test Cloud Storage
curl "https://storage.googleapis.com/<bucket>/"
```

## Important Notes

- APKs can be extracted from any device — "internal" apps are not protected
- Read-only database access is NOT automatically safe (data exfiltration is possible)
- Anonymous authentication enables automated attack scaling
- Always document testing activity for responsible disclosure

## Reference

See [vulnerabilities.md](references/vulnerabilities.md) for detailed vulnerability descriptions and remediation guidance.
