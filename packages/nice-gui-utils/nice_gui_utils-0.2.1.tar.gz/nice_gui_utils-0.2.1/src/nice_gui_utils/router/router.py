from functools import singledispatchmethod
from typing import Callable, Dict, Optional, AnyStr, Union, Any

from nicegui import background_tasks, helpers, ui


class _RouterFrame(ui.element, component='router_frame.js'):

    def __init__(self, check_interval: int):
        super().__init__()

        props: Dict[AnyStr, Any] = self._props
        props['checkInterval'] = check_interval

    def update_history(self, path):
        self.run_method('updateHistory', path)


class Router:

    def __init__(self, check_interval: int = None) -> None:
        self.routes: Dict[AnyStr, Callable] = {}
        self.content: Optional[ui.element] = None
        self.router_frame: _RouterFrame = _RouterFrame(check_interval if check_interval else 10)

    def path(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func

        return decorator

    @singledispatchmethod
    def go_to(self, target: Union[Callable, AnyStr]):
        path = {target: path for path, target in self.routes.items()}[target]
        self.go_to(path)

    @go_to.register
    def _(self, target: str):
        path = target
        builder = self.routes[target]

        async def build() -> None:
            with self.content:
                self.router_frame.update_history(path)
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result

        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = self.router_frame.on('open', lambda e: self.go_to(e.args))
        return self.content
