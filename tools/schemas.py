import inspect
from collections.abc import Callable
from typing import Any

from openai.types.responses import FunctionToolParam
from pydantic import TypeAdapter


def tool_schema(fn: Callable[..., Any]) -> FunctionToolParam:
    return {
        "type": "function",
        "name": fn.__name__,
        "description": inspect.getdoc(fn),
        "parameters": TypeAdapter(fn).json_schema(),  # type: ignore[arg-type]
        "strict": False,
    }
