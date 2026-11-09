import itertools
import threading


class Spinner:
    FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, label: str = "thinking...") -> None:
        self.label = label
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        for f in itertools.cycle(self.FRAMES):
            print(f"\r{f} {self.label}", end="", flush=True)
            if self._stop.wait(0.1):
                break
        print("\r\033[2K", end="", flush=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.stop()
