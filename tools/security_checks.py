from tools.http_client import send_request


def check_idor(base_url, attacker_token, victim_id):
    path = f"/api/users/{victim_id}"

    response = send_request(
        base_url,
        "GET",
        path,
        attacker_token,
    )

    body = response["body"]
    exposed = (
        response["status_code"] == 200
        and isinstance(body, dict)
        and body.get("id") == victim_id
    )

    return {
        "check": "idor",
        "endpoint": path,
        "status_code": response["status_code"],
        "potential_vulnerability": exposed,
        "evidence": (
            "Authenticated user accessed another user's record"
            if exposed else "No unauthorized record access confirmed"
        ),
    }


def check_admin_access(base_url, user_token):
    path = "/api/admin/stats"

    response = send_request(
        base_url,
        "GET",
        path,
        user_token,
    )

    exposed = (
        response["status_code"] == 200
        and isinstance(response["body"], dict)
        and response["body"].get("internal") is True
    )

    return {
        "check": "broken_function_level_authorization",
        "endpoint": path,
        "status_code": response["status_code"],
        "potential_vulnerability": exposed,
        "evidence": (
            "Regular user accessed an admin-only endpoint"
            if exposed else "Admin endpoint access not confirmed"
        ),
    }