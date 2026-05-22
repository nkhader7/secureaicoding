# ASVS v5 Domain Skill Map

Use the domains below as modular "skills" when converting requirements into verification tasks.

## V1 Architecture, Design and Threat Modeling
- Define security context, trust boundaries, data flows, and abuse cases.
- Verify threat modeling exists and is updated per major architecture change.

## V2 Authentication
- Verify identity proofing, login controls, MFA requirements, and anti-automation defenses.

## V3 Session Management
- Verify session creation, rotation, expiration, logout behavior, and token protections.

## V4 Access Control
- Verify authorization checks are server-side, deny-by-default, and object/function level controls are enforced.

## V5 Validation, Sanitization and Encoding
- Verify input constraints, canonicalization, context-aware output encoding, and parser safety.

## V6 Stored Cryptography
- Verify key management, approved algorithms, random generation, and secret lifecycle.

## V7 Error Handling and Logging
- Verify safe error messages, tamper-evident audit trails, and alerting for security-relevant events.

## V8 Data Protection
- Verify data classification, minimization, retention, masking, and secure deletion.

## V9 Communication Security
- Verify transport security, certificate validation, and channel protections.

## V10 Malicious Code and File Handling
- Verify file upload validation, malware scanning, sandboxing, and content-type enforcement.

## V11 Business Logic
- Verify anti-abuse controls, rate/velocity limits, workflow integrity, and fraud resistance.

## V12 API and Web Service
- Verify API authentication/authorization, schema validation, replay defenses, and safe defaults.

## V13 Configuration
- Verify hardening baselines, secure defaults, and configuration drift detection.

## V14 Build and Deployment
- Verify supply-chain controls, build integrity, artifact signing, and deployment separation.

## V15 Secure Development Lifecycle
- Verify secure SDLC activities (training, reviews, testing gates, dependency management).

## V16 Privacy and Compliance
- Verify consent, purpose limitation, data-subject rights flows, and privacy-by-design controls.
