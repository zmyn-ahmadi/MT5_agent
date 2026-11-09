import json

from openai import OpenAI
from pydantic import validate_call
from rich.console import Console
from rich.markdown import Markdown

from spinner import Spinner
from tools.schemas import tool_schema

console = Console()


class LLM:
    def __init__(
        self,
        base_url,
        api_key="none",
        model="local",
        stream=True,
        tools=None,
        max_messages=8192,
        instructions="",
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.stream = stream
        self.instructions = instructions

        self.history = []
        self.max_messages = max_messages

        tools = tools or []
        self.tools = [tool_schema(fn) for fn in tools]  # list of tools json
        self.tool_fns = {
            fn.__name__: validate_call(fn) for fn in tools
        }  # {"function name": fn}

    def chat(self):
        while True:
            try:
                user_input = input("> ")
            except (KeyboardInterrupt, EOFError):
                print()
                break

            if not user_input.strip():
                continue

            self._trim_history()
            start = len(self.history)
            self.history.append({"role": "user", "content": user_input})

            try:
                reply = self._run_turn()
            except KeyboardInterrupt:
                del self.history[start:]  # forget the unfinished turn
                print()
                continue
            except Exception as e:
                del self.history[start:]
                console.print(f"[red]Error:[/red] {e}")
                continue

            self.history.append(
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": reply}],
                }
            )
            console.print("\n", Markdown(reply))

    def _run_turn(self):
        """Ask the model, run any tools it calls, repeat until it answers in text."""
        seen = set()

        while True:
            response = self._reply()
            calls = [item for item in response.output if item.type == "function_call"]

            if not calls:
                return response.output_text or ""

            for call in calls:
                # Local models repeat calls, and each full copy eats the context.
                key = (call.name, call.arguments)
                if key in seen:
                    output = (
                        '{"note": "Same call already returned above. Use that result."}'
                    )
                else:
                    output = self._run_tool(call)
                seen.add(key)

                self.history.append(
                    {
                        "type": "function_call",
                        "call_id": call.call_id,
                        "name": call.name,
                        "arguments": call.arguments,
                    }
                )
                self.history.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": output,
                    }
                )

    def _run_tool(self, call):
        try:
            args = json.loads(call.arguments or "{}")
            return json.dumps(self.tool_fns[call.name](**args))
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _reply(self):
        with Spinner():
            response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                input=self.history,
                tools=self.tools,
                stream=self.stream,
            )
            if not self.stream:
                return response

            for event in response:
                if event.type == "response.completed":
                    return event.response

        raise RuntimeError("Stream ended without a completed response")

    def _trim_history(self):
        # ponytail: counts messages, not tokens; use a real tokenizer if context overflows.
        if len(self.history) > self.max_messages:
            self.history = self.history[-10:]
