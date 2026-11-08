"""Add or update a teacher account without storing a plaintext password."""

import getpass
import json
from pathlib import Path

from .auth import (
    TEACHERS_EXAMPLE_FILE,
    TEACHERS_FILE,
    hash_password,
    load_teachers,
)


def main() -> None:
    username = input("Teacher username: ").strip()
    if not username:
        raise ValueError("Username cannot be empty")

    password = getpass.getpass("Teacher password: ")
    confirmation = getpass.getpass("Confirm password: ")
    if not password:
        raise ValueError("Password cannot be empty")
    if password != confirmation:
        raise ValueError("Passwords do not match")

    teachers = load_teachers(
        TEACHERS_FILE if TEACHERS_FILE.exists() else TEACHERS_EXAMPLE_FILE
    )
    updated = False
    for teacher in teachers:
        if teacher["username"] == username:
            teacher["password_hash"] = hash_password(password)
            updated = True
            break
    if not updated:
        teachers.append({
            "username": username,
            "password_hash": hash_password(password),
        })

    temporary_file = Path(f"{TEACHERS_FILE}.tmp")
    temporary_file.write_text(
        json.dumps({"teachers": teachers}, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_file.replace(TEACHERS_FILE)
    print(f"Teacher account {'updated' if updated else 'added'}: {username}")


if __name__ == "__main__":
    main()
