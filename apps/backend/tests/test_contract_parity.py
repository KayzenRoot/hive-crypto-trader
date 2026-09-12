import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.validate_contract_parity import main


def test_canonical_and_runtime_contracts_have_parity() -> None:
    assert main() == 0
