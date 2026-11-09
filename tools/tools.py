from typing import Any

import httpx
import dotenv
import os
import pathlib

dotenv.load_dotenv()


base_url = os.getenv("MT5_API_URL")
token = os.getenv("MT5_API_TOKEN")


def get_history() -> list[dict[str, Any]] | dict[str, str]:
    """Fetch historical records from the history API. Use when the user asks
    about past events, previous entries, or changes over time.
    Returns a list of records, newest first."""

    HISTORY_FIELDS = ("time", "symbol", "type", "entry", "price", "profit")

    try:
        r = httpx.get(
            f"{base_url}/history/deals?days=346",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        r.raise_for_status()
        return [{k: deal.get(k) for k in HISTORY_FIELDS} for deal in r.json()]
    except httpx.HTTPStatusError as e:
        return {
            "error": f"API returned {e.response.status_code}: {e.response.text[:200]}"
        }
    except httpx.RequestError as e:
        return {"error": f"Request faild: {e}"}


ROOT = pathlib.Path("./data").resolve()


def _safe(path: str) -> pathlib.Path:
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError("path outside workspace")
    return p


def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    return _safe(path).read_text()[:20000]


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating it if needed."""
    p = _safe(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return f"wrote {len(content)} chars to {path}"
