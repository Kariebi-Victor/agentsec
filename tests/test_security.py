
import pytest

from tools.security_checks import check_idor, check_admin_access


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module", autouse=True)
def require_test_server():
    import httpx

    try:
        response = httpx.get(BASE_URL, timeout=3)
        response.raise_for_status()
    except httpx.HTTPError:
        pytest.fail(
            "Local test API is not running. "
            "Start it with: python -m uvicorn "
            "vulnerable_api.main:app --host 127.0.0.1 --port 8000"
        )


def test_idor_detection():
    result = check_idor(
        BASE_URL,
        attacker_token="alice-token",
        victim_id=2,
    )

    assert result["potential_vulnerability"] is True
    assert result["status_code"] == 200
    assert result["check"] == "idor"


def test_broken_admin_authorization():
    result = check_admin_access(
        BASE_URL,
        user_token="alice-token",
    )

    assert result["potential_vulnerability"] is True
    assert result["status_code"] == 200
    assert result["check"] == "broken_function_level_authorization"


def test_invalid_token_does_not_confirm_idor():
    result = check_idor(
        BASE_URL,
        attacker_token="invalid-token",
        victim_id=2,
    )

    assert result["potential_vulnerability"] is False
    assert result["status_code"] == 401


def test_invalid_token_does_not_confirm_admin_access():
    result = check_admin_access(
        BASE_URL,
        user_token="invalid-token",
    )

    assert result["potential_vulnerability"] is False
    assert result["status_code"] == 401
