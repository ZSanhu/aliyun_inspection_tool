def check_ram_inactive():
    users = [
        {"username": "ops-dev", "logged_in": False, "ak_used": False},
        {"username": "admin", "logged_in": True, "ak_used": True},
        {"username": "readonly", "logged_in": True, "ak_used": False}
    ]
    result = []
    for u in users:
        status = "异常（长期未用）" if not u["logged_in"] or not u["ak_used"] else "正常"
        result.append([
            u["username"],
            "否" if not u["logged_in"] else "是",
            "否" if not u["ak_used"] else "是",
            status
        ])
    return result
