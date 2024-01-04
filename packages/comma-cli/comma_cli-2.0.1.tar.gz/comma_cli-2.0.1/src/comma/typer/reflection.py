#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from contextlib import suppress
from typing import Any
from typing import Callable
from typing import Generator
from typing import NamedTuple
from typing import Sequence

import typer
from comma.command import Command
from fzf import fzf
from typer.models import ArgumentInfo


class TyperNode(NamedTuple):
    path: tuple[str, ...]
    func: Callable[..., Any] | None
    name: str
    doc: str
    level: int

    def print_source(self) -> None:
        if not self.func:
            return
        try:
            import inspect

            _, line_num = inspect.findsource(self.func)
            code = inspect.getsource(self.func)
            filename = inspect.getfile(self.func)
            width = max(len(x) for x in code.splitlines())
            from rich import print as rprint

            rprint(f"{filename}:{line_num + 1}")
            from rich.syntax import Syntax

            rprint(
                Syntax(
                    code,
                    "python",
                    code_width=width,
                    theme="ansi_dark",
                ),
            )
        except TypeError:
            return

    @classmethod
    def traverse_nodes(
        cls,
        app: typer.Typer,
        root_name: str = "",
        path: tuple[str, ...] = (),
        _level: int = 0,
    ) -> Generator[TyperNode, None, None]:
        app_name = app.info.name or root_name
        path = (*path, app_name)
        yield TyperNode(
            path=path,
            func=app,
            name=app_name,
            doc=app.info.help or "",
            level=_level,
        )
        for command in app.registered_commands:
            func = command.callback
            if func:
                func_name = command.name or func.__name__.replace("_", "-")
                doc = command.help or func.__doc__ or "NO DOC"
                yield TyperNode(
                    path=(*path, func_name),
                    func=func,
                    name=func_name,
                    doc=doc,
                    level=_level + 1,
                )
        for group in app.registered_groups:
            if group.typer_instance:
                yield from cls.traverse_nodes(group.typer_instance, _level=_level + 1, path=path)

    def execute(self, *args: str, _print_cmd: bool = False) -> None:
        # Check if root command is in the path
        root_executable: tuple[str, ...] = (shutil.which(self.path[0]),)  # type: ignore
        if root_executable[0] is None:
            root_executable = (sys.argv[0],)
            with suppress(Exception):
                import inspect
                from comma import main

                root_executable = (sys.executable, inspect.getfile(main))
        Command(
            cmd=(
                *root_executable,
                *self.path[1:],
                *args,
            ),
        ).execvp(log_command=_print_cmd)


app_reflection = typer.Typer(name="reflection", help="Reflect on the CLI.")


def _traverse_nodes_() -> Generator[TyperNode, None, None]:
    from comma.main import app_main

    yield from TyperNode.traverse_nodes(app_main, root_name="dev")


def _pick_node_() -> TyperNode | None:
    return fzf(
        _traverse_nodes_(),
        key=lambda x: f'{" ".join(x.path)} --> {x.doc.strip().splitlines()[0]}',
    )


typer_settigs = {
    "add_help_option": False,
    "no_args_is_help": False,
    "context_settings": {
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
}


@app_reflection.command(**typer_settigs, name="show")
def show_func() -> None:
    """Show function source code."""
    node = _pick_node_()
    if node:
        node.print_source()
        if node.path[-1] not in ("run", "show"):
            node.execute("--help", _print_cmd=True)


@app_reflection.command(**typer_settigs, name="tree")
def tree() -> None:
    """Show all functions."""
    nodes = list(_traverse_nodes_())
    width = max(len(" ".join(x.path)) for x in nodes)
    for x in nodes:
        print(
            f'{" ".join(x.path):<{width}} --> {x.doc.strip().splitlines()[0]}',
        )


@app_reflection.command(**typer_settigs, name="run")
def run_func(
    ctx: typer.Context = typer.Argument(None),  # noqa: B008
) -> None:
    """Select function interactively and run it."""
    node = _pick_node_()
    if not node:
        return
    args: Sequence[str] = ctx.args if ctx and not isinstance(ctx, ArgumentInfo) else sys.argv[1:]
    node.execute(*args, _print_cmd=True)


if __name__ == "__main__":
    app_reflection()
