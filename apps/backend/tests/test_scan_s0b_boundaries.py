import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s0b_boundaries as scanner


@pytest.mark.parametrize(
    "signature",
    [
        lambda: "gh" + "p_" + "a" * 36,
        lambda: "github" + "_pat_" + "b" * 30,
        lambda: "AKIA" + "C" * 16,
        lambda: "-----BEGIN " + "PRIVATE KEY-----",
        lambda: "token = '" + "x" * 20 + "'",
    ],
)
def test_secret_signatures_are_detected_without_repository_literals(signature) -> None:
    assert scanner.scan_secret_text("apps/backend/tests/synthetic.py", signature())


def test_opaque_reference_identifiers_are_not_flagged() -> None:
    text = 'CredentialRef("cred-ref-account-a") SecretRef("secret-ref-audit-a")'
    assert scanner.scan_secret_text("apps/backend/tests/synthetic.py", text) == []


def test_capability_scan_is_separate_from_secret_scan() -> None:
    text = "token = '" + "x" * 20 + "'"
    assert scanner.scan_secret_text("apps/backend/tests/synthetic.py", text)
    assert scanner.scan_capability_text("apps/backend/tests/synthetic.py", text) == []


def test_unreadable_changed_candidate_fails_closed(tmp_path, monkeypatch) -> None:
    candidate = tmp_path / "candidate.py"
    candidate.write_bytes(b"not utf8: \xff")
    monkeypatch.setattr(scanner, "ROOT", tmp_path)
    with pytest.raises(scanner.BoundaryScanError, match="not readable UTF-8 text"):
        scanner.read_changed_text("candidate.py")
