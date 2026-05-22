# ASVS v5 Mapping Template

| ASVS Domain | Requirement/Control | Verification Activity | Evidence | Owner | Status | Notes |
|---|---|---|---|---|---|---|
| V4 Access Control | Enforce server-side authZ checks on protected actions | Unit tests + integration tests + manual negative test | Test report link | AppSec + Service Team | Pass/Fail/Waived | Residual risk / exception expiry |
| V6 Stored Cryptography | Keys stored and rotated using managed KMS | IaC review + runtime config validation | Terraform plan + config snapshot | Platform Team | Pass/Fail/Waived | Rotation interval |

## Status Definitions
- **Pass**: Requirement fully implemented and verified.
- **Fail**: Requirement not met or verification failed.
- **Waived**: Approved risk exception with expiration date and compensating controls.
