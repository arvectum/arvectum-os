#!/usr/bin/env python3
"""P6.05-L3 secret-safe local configuration preflight.

This is a bounded owner-operated validation helper for the current P6.05 local
runtime. It validates a non-secret local configuration file and a separately
stored EIS token file without printing, hashing, persisting, exporting, or
otherwise recording the secret value. It performs no product invocation, EIS
request, network action, canonical mutation, or external action.
"""

from __future__ import annotations

import argparse
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


MAX_LOCAL_FILE_BYTES = 64 * 1024
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
FALSE_VALUES = frozenset({"0", "false", "no", "off"})
PLACEHOLDER_SECRET_VALUES = frozenset(
    {
        "",
        "replace_me",
        "replace_me_do_not_commit_real_token",
        "insert_token_here",
        "change_me",
        "changeme",
        "вставить_токен_сюда",
    }
)
SECRET_ENV_KEY = "ZAKUPKI_GOV_RU_SOAP_TOKEN"
REQUIRED_CONTROLS = {
    "ZAKUPKI_GOV_RU_SOAP_ENABLED": True,
    "ZAKUPKI_GOV_RU_SOAP_DISABLE_PROXY_FOR_EIS": True,
    "ZAKUPKI_GOV_RU_SOAP_REQUIRE_DIRECT_RU_ROUTE": True,
    "ZAKUPKI_GOV_RU_SOAP_TRUST_ENV_PROXY": False,
    "ZAKUPKI_GOV_RU_SOAP_DEBUG": False,
}
REQUIRED_LITERAL_CONTROLS = {
    "ZAKUPKI_GOV_RU_SOAP_TOKEN_OWNER": "individual",
}
ALLOWED_CONFIG_KEYS = frozenset((*REQUIRED_CONTROLS, *REQUIRED_LITERAL_CONTROLS))


class PreflightError(RuntimeError):
    """Safe validation error that contains no local configuration values."""

    def __init__(self, code: str, subject: str | None = None) -> None:
        self.code = code
        self.subject = subject
        message = code if subject is None else f"{code}: {subject}"
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class LocalFileMetadata:
    path: Path
    directory_owner_only: bool
    file_owner_only: bool


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _owner_only(mode: int) -> bool:
    return mode & 0o077 == 0


def inspect_external_owner_only_file(
    path: Path,
    *,
    repo_root: Path | None = None,
    kind: str,
) -> LocalFileMetadata:
    repo = (repo_root or _repo_root()).resolve(strict=True)
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise PreflightError(f"{kind}_SYMLINK_NOT_ALLOWED")
    if expanded.parent.is_symlink():
        raise PreflightError(f"{kind}_DIRECTORY_SYMLINK_NOT_ALLOWED")

    resolved = expanded.resolve(strict=False)
    if _is_relative_to(resolved, repo):
        raise PreflightError(f"{kind}_INSIDE_SOURCE_CONTROL")
    if not resolved.exists():
        raise PreflightError(f"{kind}_NOT_FOUND")
    if not resolved.is_file():
        raise PreflightError(f"{kind}_NOT_REGULAR_FILE")

    parent = resolved.parent
    if not parent.is_dir():
        raise PreflightError(f"{kind}_DIRECTORY_INVALID")

    file_mode = stat.S_IMODE(resolved.stat().st_mode)
    directory_mode = stat.S_IMODE(parent.stat().st_mode)
    if not _owner_only(file_mode):
        raise PreflightError(f"{kind}_FILE_PERMISSIONS_TOO_BROAD")
    if not _owner_only(directory_mode):
        raise PreflightError(f"{kind}_DIRECTORY_PERMISSIONS_TOO_BROAD")
    if resolved.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise PreflightError(f"{kind}_FILE_TOO_LARGE")

    return LocalFileMetadata(
        path=resolved,
        directory_owner_only=True,
        file_owner_only=True,
    )


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_nonsecret_config(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PreflightError("CONFIG_NOT_UTF8") from exc
    except OSError as exc:
        raise PreflightError("CONFIG_READ_FAILED") from exc

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            raise PreflightError("SHELL_SYNTAX_NOT_ALLOWED", f"line-{line_number}")
        if "=" not in stripped:
            raise PreflightError("MALFORMED_CONFIG_LINE", f"line-{line_number}")
        key, raw_value = stripped.split("=", 1)
        key = key.strip()
        if not KEY_RE.fullmatch(key):
            raise PreflightError("INVALID_CONFIG_KEY", f"line-{line_number}")
        if key in values:
            raise PreflightError("DUPLICATE_CONFIG_KEY", key)
        if key == SECRET_ENV_KEY:
            raise PreflightError("SECRET_VALUE_IN_NONSECRET_CONFIG", key)
        if key not in ALLOWED_CONFIG_KEYS:
            raise PreflightError("UNDECLARED_CONFIG_KEY", key)
        values[key] = _unquote(raw_value.strip())
    return values


def validate_secret_file(path: Path) -> None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError as exc:
        raise PreflightError("SECRET_NOT_UTF8", SECRET_ENV_KEY) from exc
    except OSError as exc:
        raise PreflightError("SECRET_READ_FAILED", SECRET_ENV_KEY) from exc
    if not value or value.lower() in PLACEHOLDER_SECRET_VALUES:
        raise PreflightError("SECRET_NOT_CONFIGURED", SECRET_ENV_KEY)
    if "\n" in value or "\r" in value:
        raise PreflightError("SECRET_FORMAT_INVALID", SECRET_ENV_KEY)


def _parse_bool_control(values: Mapping[str, str], key: str) -> bool:
    if key not in values:
        raise PreflightError("MISSING_REQUIRED_CONTROL", key)
    normalized = values[key].strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise PreflightError("INVALID_BOOLEAN_CONTROL", key)


def validate_required_controls(values: Mapping[str, str]) -> None:
    for key, expected in REQUIRED_CONTROLS.items():
        if _parse_bool_control(values, key) is not expected:
            raise PreflightError("CONTROL_MISMATCH", key)

    for key, expected in REQUIRED_LITERAL_CONTROLS.items():
        if key not in values:
            raise PreflightError("MISSING_REQUIRED_CONTROL", key)
        if values[key].strip().lower() != expected:
            raise PreflightError("CONTROL_MISMATCH", key)


def _safe_summary_lines(*, status: str, failure: PreflightError | None = None) -> list[str]:
    lines = [
        f"p6_05_l3_status={status}",
        "operational_environment=Internal / local owner-operated runtime",
        "production_readiness_claim=None",
        "configuration_source=external_nonsecret_local_file",
        "secret_source=separate_external_owner_only_file",
    ]
    if status == "PASS":
        lines.extend(
            (
                "config_outside_source_control=true",
                "config_directory_owner_only=true",
                "config_file_owner_only=true",
                "secret_outside_source_control=true",
                "secret_directory_owner_only=true",
                "secret_file_owner_only=true",
                f"secret.{SECRET_ENV_KEY}=configured",
            )
        )
        lines.extend(f"control.{key}=expected" for key in REQUIRED_CONTROLS)
        lines.extend(f"control.{key}=expected" for key in REQUIRED_LITERAL_CONTROLS)
    elif failure is not None:
        lines.append(f"failure_code={failure.code}")
        if failure.subject:
            lines.append(f"failure_subject={failure.subject}")
    lines.extend(
        (
            "secret_values_printed=false",
            "secret_values_hashed=false",
            "secret_values_persisted_by_preflight=false",
            "product_invoked=false",
            "eis_invoked=false",
            "network_invoked=false",
            "external_actions=false",
        )
    )
    return lines


def run_preflight(
    config_path: Path,
    secret_path: Path,
    *,
    repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    try:
        config_metadata = inspect_external_owner_only_file(
            config_path,
            repo_root=repo_root,
            kind="CONFIG",
        )
        secret_metadata = inspect_external_owner_only_file(
            secret_path,
            repo_root=repo_root,
            kind="SECRET",
        )
        values = parse_nonsecret_config(config_metadata.path)
        validate_required_controls(values)
        validate_secret_file(secret_metadata.path)
    except PreflightError as exc:
        return 2, tuple(_safe_summary_lines(status="FAIL", failure=exc))
    return 0, tuple(_safe_summary_lines(status="PASS"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the bounded P6.05-L3 local config/secrets boundary without printing secret values."
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to the non-secret local configuration file outside the Arvectum OS checkout.",
    )
    parser.add_argument(
        "--eis-token-file",
        required=True,
        type=Path,
        help="Path to the owner-only local EIS token file outside source-controlled checkouts.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = run_preflight(args.config, args.eis_token_file)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
