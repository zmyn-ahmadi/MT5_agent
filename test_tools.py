import json
from types import SimpleNamespace
from typing import Annotated, Any

from pydantic import Field

from llm import LLM
from tools.tools import get_history


def add(
    a: int, b: Annotated[int, Field(ge=0, description="Must not be negative")] = 1
) -> int:
    """Add two numbers."""
    return a + b


def run(llm: LLM, arguments: str) -> Any:
    call: Any = SimpleNamespace(name="add", arguments=arguments)
    return json.loads(llm._run_tool(call))


if __name__ == "__main__":
    llm = LLM(base_url="http://unused/v1", tools=[add, get_history])
    schemas: list[Any] = llm.tools
    add_schema, history_schema = schemas

    assert add_schema["name"] == "add"
    assert add_schema["description"] == "Add two numbers."
    assert add_schema["parameters"]["required"] == ["a"]
    assert add_schema["parameters"]["properties"]["b"]["minimum"] == 0
    assert history_schema["parameters"]["properties"] == {}
    assert history_schema["description"].startswith("Fetch historical records")

    assert run(llm, '{"a": 2, "b": 3}') == 5
    assert run(llm, '{"a": "2"}') == 3  # pydantic coerces model-supplied strings
    assert "error" in run(llm, '{"a": 2, "b": -1}')
    assert "error" in run(llm, '{"a": 2, "nope": 1}')
    assert "error" in run(llm, "{}")

    ran: list[int] = []

    def ping(n: int = 0) -> int:
        """Record a call."""
        ran.append(n)
        return n

    def call(n: int) -> Any:
        return SimpleNamespace(
            type="function_call", call_id=f"c{n}", name="ping", arguments=f'{{"n": {n}}}'
        )

    def response(*output: Any) -> Any:
        return SimpleNamespace(output=output, output_text="done")

    llm = LLM(base_url="http://unused/v1", stream=False, tools=[ping])
    replies = iter([response(call(1), call(1)), response(call(1)), response(call(2)), response()])
    llm._reply = lambda: next(replies)  # type: ignore[method-assign]

    assert llm._run_turn() == "done"
    assert ran == [1, 2]  # repeats, same response or later, don't re-run
    outputs = [i["output"] for i in llm.history if i["type"] == "function_call_output"]
    assert len(outputs) == 4 and outputs[1] == outputs[2] and "already" in outputs[1]
    print("ok")
