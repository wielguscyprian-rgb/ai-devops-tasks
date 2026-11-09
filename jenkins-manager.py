#!/usr/bin/env python3
"""Klient Jenkins REST API: lista zadań, status buildów, uruchamianie joba."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


COLOR_STATUS = {
    "blue": "SUCCESS",
    "blue_anime": "SUCCESS (buduje się)",
    "green": "SUCCESS",
    "green_anime": "SUCCESS (buduje się)",
    "red": "FAILURE",
    "red_anime": "FAILURE (buduje się)",
    "yellow": "UNSTABLE",
    "yellow_anime": "UNSTABLE (buduje się)",
    "grey": "NOT_BUILT",
    "grey_anime": "NOT_BUILT (buduje się)",
    "disabled": "DISABLED",
    "aborted": "ABORTED",
    "aborted_anime": "ABORTED (buduje się)",
    "notbuilt": "NOT_BUILT",
    "notbuilt_anime": "NOT_BUILT (buduje się)",
}


class JenkinsError(Exception):
    """Błąd komunikacji z Jenkinsem lub niepoprawnej odpowiedzi API."""


class JenkinsClient:
    def __init__(self, base_url: str, user: str, token: str, timeout: float = 30.0) -> None:
        if not base_url or not user or not token:
            raise JenkinsError(
                "Brak konfiguracji. Ustaw JENKINS_URL, JENKINS_USER i JENKINS_TOKEN "
                "(token API z profilu użytkownika w Jenkinsie)."
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(user, token)
        self.session.headers.update({"Accept": "application/json"})
        self._crumb: tuple[str, str] | None = None

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        try:
            response = self.session.request(
                method,
                self._url(path),
                timeout=self.timeout,
                **kwargs,
            )
        except requests.Timeout as exc:
            raise JenkinsError(f"Przekroczono czas oczekiwania na {self.base_url}") from exc
        except requests.ConnectionError as exc:
            raise JenkinsError(f"Nie można połączyć się z Jenkinsem ({self.base_url})") from exc
        except requests.RequestException as exc:
            raise JenkinsError(f"Błąd żądania HTTP: {exc}") from exc

        if response.status_code in (401, 403):
            raise JenkinsError(
                f"Odmowa dostępu ({response.status_code}). "
                "Sprawdź użytkownika, token API i uprawnienia do zadania."
            )
        return response

    def _json(self, response: requests.Response) -> Any:
        if response.status_code == 404:
            raise JenkinsError("Nie znaleziono zasobu w Jenkinsie (404).")
        if not response.ok:
            body = (response.text or "").strip().replace("\n", " ")[:300]
            raise JenkinsError(f"Jenkins zwrócił HTTP {response.status_code}: {body}")
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise JenkinsError("Odpowiedź Jenkinsa nie jest poprawnym JSON-em.") from exc

    def _crumb_headers(self) -> dict[str, str]:
        """Pobiera crumb CSRF wymagany przy POST (build)."""
        if self._crumb is not None:
            field, value = self._crumb
            return {field: value}

        response = self._request("GET", "/crumbIssuer/api/json")
        if response.status_code == 404:
            return {}
        data = self._json(response)
        field = data.get("crumbRequestField")
        value = data.get("crumb")
        if not field or not value:
            raise JenkinsError("Jenkins nie zwrócił poprawnego crumb CSRF.")
        self._crumb = (field, value)
        return {field: value}

    def list_jobs(self) -> list[dict[str, Any]]:
        data = self._json(
            self._request("GET", "/api/json", params={"tree": "jobs[name,url,color]"})
        )
        jobs = data.get("jobs") if isinstance(data, dict) else None
        if not isinstance(jobs, list):
            raise JenkinsError("Nieoczekiwany format listy zadań.")
        return jobs

    def recent_builds(self, job_name: str, count: int) -> list[dict[str, Any]]:
        tree = f"builds[number,result,building,timestamp,duration,url]{{0,{count}}}"
        data = self._json(
            self._request("GET", f"/{job_api_path(job_name)}/api/json", params={"tree": tree})
        )
        builds = data.get("builds") if isinstance(data, dict) else None
        if not isinstance(builds, list):
            raise JenkinsError(f"Nieoczekiwany format buildów dla zadania '{job_name}'.")
        return builds

    def trigger(self, job_name: str, parameters: dict[str, str] | None = None) -> str:
        path = job_api_path(job_name)
        headers = self._crumb_headers()
        if parameters:
            response = self._request(
                "POST",
                f"/{path}/buildWithParameters",
                headers=headers,
                data=parameters,
            )
        else:
            response = self._request(
                "POST",
                f"/{path}/build",
                headers=headers,
            )

        if response.status_code == 404:
            raise JenkinsError(f"Zadanie '{job_name}' nie istnieje.")
        if response.status_code not in (200, 201):
            body = (response.text or "").strip().replace("\n", " ")[:300]
            raise JenkinsError(
                f"Nie udało się uruchomić '{job_name}' (HTTP {response.status_code}): {body}"
            )
        location = response.headers.get("Location", "")
        return location or f"{self.base_url}/{path}/"


def job_api_path(job_name: str) -> str:
    """Zamienia 'folder/zadanie' na 'job/folder/job/zadanie'."""
    parts = [part.strip() for part in job_name.strip("/").split("/") if part.strip()]
    if not parts:
        raise JenkinsError("Nazwa zadania jest pusta.")
    return "/".join(f"job/{requests.utils.quote(part, safe='')}" for part in parts)


def color_to_status(color: str | None) -> str:
    if not color:
        return "UNKNOWN"
    return COLOR_STATUS.get(color, color.upper())


def parse_parameters(items: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise JenkinsError(f"Parametr '{item}' musi mieć postać KLUCZ=WARTOŚĆ.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise JenkinsError(f"Pusty klucz w parametrze '{item}'.")
        params[key] = value
    return params


def cmd_list(client: JenkinsClient) -> int:
    jobs = client.list_jobs()
    if not jobs:
        print("Brak zadań.")
        return 0
    name_width = max(len(str(job.get("name", ""))) for job in jobs)
    print(f"{'ZADANIE':<{name_width}}  STATUS")
    for job in jobs:
        name = str(job.get("name", ""))
        status = color_to_status(job.get("color"))
        print(f"{name:<{name_width}}  {status}")
    return 0


def cmd_status(client: JenkinsClient, job: str | None, count: int) -> int:
    if job:
        names = [job]
    else:
        names = [str(item.get("name", "")) for item in client.list_jobs() if item.get("name")]

    if not names:
        print("Brak zadań.")
        return 0

    exit_code = 0
    for name in names:
        print(f"\n{name}")
        try:
            builds = client.recent_builds(name, count)
        except JenkinsError as exc:
            print(f"  Błąd: {exc}")
            exit_code = 1
            continue
        if not builds:
            print("  brak buildów")
            continue
        for build in builds:
            number = build.get("number", "?")
            if build.get("building"):
                result = "BUILDING"
            else:
                result = build.get("result") or "UNKNOWN"
            url = build.get("url", "")
            print(f"  #{number:<6} {result:<10} {url}")
    return exit_code


def cmd_build(client: JenkinsClient, job: str, parameters: dict[str, str]) -> int:
    queue_url = client.trigger(job, parameters or None)
    print(f"Uruchomiono '{job}'.")
    print(f"Kolejka: {queue_url}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Zarządzanie zadaniami Jenkinsa przez REST API."
    )
    parser.add_argument("--url", default=os.environ.get("JENKINS_URL", ""), help="Adres Jenkinsa")
    parser.add_argument("--user", default=os.environ.get("JENKINS_USER", ""), help="Użytkownik")
    parser.add_argument(
        "--token",
        default=os.environ.get("JENKINS_TOKEN", ""),
        help="Token API (lepiej przez zmienną JENKINS_TOKEN)",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout HTTP w sekundach")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Wypisz wszystkie zadania i status ostatniego builda")

    status = sub.add_parser("status", help="Status ostatnich buildów")
    status.add_argument("--job", help="Nazwa jednego zadania (domyślnie wszystkie)")
    status.add_argument("--count", type=int, default=5, help="Ile ostatnich buildów pokazać")

    build = sub.add_parser("build", help="Uruchom wybrane zadanie")
    build.add_argument("job", help="Nazwa zadania")
    build.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="KLUCZ=WARTOŚĆ",
        help="Parametr builda (można podać wielokrotnie)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = JenkinsClient(args.url, args.user, args.token, timeout=args.timeout)
        if args.command == "list":
            return cmd_list(client)
        if args.command == "status":
            if args.count < 1:
                raise JenkinsError("--count musi być większe od 0.")
            return cmd_status(client, args.job, args.count)
        if args.command == "build":
            return cmd_build(client, args.job, parse_parameters(args.param))
        raise JenkinsError(f"Nieznana komenda: {args.command}")
    except JenkinsError as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
