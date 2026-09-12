"""Generated from packages/contracts/openapi.json; do not edit."""

CONTRACT_SHA256 = "43e98281de732e5c81ef9d8683a92cac369634a57032e2ced7682882568c88b6"
ENVIRONMENTS = ('LIVE', 'PAPER', 'SHADOW', 'REPLAY')
IDENTITY_KINDS = ('SERVICE', 'RELEASE', 'CONFIG', 'AUDIT', 'EVIDENCE')
ERROR_CODES = ('INVALID_REQUEST', 'NOT_READY', 'INTERNAL')
SAFE_ENDPOINTS = ('/health', '/ready', '/version')
ID_VALUE_PATTERN = r"^[a-z0-9][a-z0-9._-]{0,63}$"
EVENT_TYPE_PATTERN = r"^[A-Z][A-Z0-9_.-]{1,63}$"
HASH_PATTERN = r"^[0-9a-f]{64}$"
