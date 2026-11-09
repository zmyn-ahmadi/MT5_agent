#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["openai", "rich", "httpx", "pydantic"]
# ///

from llm import LLM
from pathlib import Path
from tools.tools import get_history, read_file, write_file


if __name__ == "__main__":
    agent = LLM(
        base_url="http://127.0.0.1:8080/v1",
        stream=True,
        tools=[get_history, read_file, write_file],
        instructions=Path("prompts/system.md").read_text(),
    )
    agent.chat()
