"""Teacher credential loading and password hashing helpers."""

import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets

TEACHERS_FILE = Path(
    os.environ.get("TEACHERS_FILE", Path(__file__).parent / "teachers.json")
)
TEACHERS_EXAMPLE_FILE = Path(__file__).parent / "teachers.example.json"
PASSWORD_HASH_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return (
        f"pbkdf2_sha256${PASSWORD_HASH_ITERATIONS}"
        f"${salt.hex()}${digest.hex()}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = password_hash.split("$")
        if algorithm != "pbkdf2_sha256" or int(iterations) != PASSWORD_HASH_ITERATIONS:
            return False
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)
    except (ValueError, TypeError):
        return False

    actual_digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return hmac.compare_digest(actual_digest, expected_digest)


def load_teachers(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as credentials_file:
        data = json.load(credentials_file)

    if not isinstance(data, dict) or not isinstance(data.get("teachers"), list):
        raise ValueError(f"{path} must contain a 'teachers' list")

    teachers = []
    usernames = set()
    for teacher in data["teachers"]:
        if (
            not isinstance(teacher, dict)
            or not isinstance(teacher.get("username"), str)
            or not teacher["username"].strip()
            or not isinstance(teacher.get("password_hash"), str)
            or not _has_valid_hash_format(teacher["password_hash"])
        ):
            raise ValueError(
                f"Each teacher in {path} must have a username and valid password_hash"
            )
        username = teacher["username"]
        if username in usernames:
            raise ValueError(f"Duplicate teacher username in {path}: {username}")
        usernames.add(username)
        teachers.append({
            "username": username,
            "password_hash": teacher["password_hash"],
        })
    return teachers


def _has_valid_hash_format(password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = password_hash.split("$")
        return (
            algorithm == "pbkdf2_sha256"
            and int(iterations) == PASSWORD_HASH_ITERATIONS
            and len(bytes.fromhex(salt_hex)) == 16
            and len(bytes.fromhex(digest_hex)) == 32
        )
    except (ValueError, TypeError):
        return False
