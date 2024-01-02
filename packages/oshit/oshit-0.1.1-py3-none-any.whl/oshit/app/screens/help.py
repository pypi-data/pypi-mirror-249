"""The help screen for the application."""

##############################################################################
# Python imports.
from inspect import cleandoc
from typing import Any
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import (  # pylint:disable=no-name-in-module
    on,
    __version__ as textual_version,
)
from textual.app import ComposeResult
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Markdown

##############################################################################
# Local imports.
from ... import __version__

##############################################################################
# The help text.
HELP = f"""\
# Orange Site Hit v{__version__}

## Introduction

OSHit is a terminal-based read-only client for [HackerNews](https://news.ycombinator.com/).

{{context_help}}

## Other

OSHit was created by and is maintained by [Dave Pearson](https://www.davep.org/).


OSHit is Free Software and can be [found on GitHub](https://github.com/davep/oshit).


This version of OSHit is using [Textual](https://textual.textualize.io/) v{textual_version}.

## Licence

OSHit - A terminal-based HackerNews reader.[EOL]
Copyright (C) 2023 Dave Pearson

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""


##############################################################################
class Help(ModalScreen[None]):
    """The help screen."""

    DEFAULT_CSS = """
    Help {
        align: center middle;
    }

    Help Vertical {
        width: 75%;
        height: 90%;
        background: $surface;
        border: panel $primary;
        border-title-color: $accent;
    }

    Help VerticalScroll {
        scrollbar-gutter: stable;
    }

    Help Center {
        height: auto;
        width: 100%;
        border-top: solid $primary;
        padding-top: 1;
    }
    """

    BINDINGS = [("escape", "close")]

    def __init__(self, help_for: Screen[Any]) -> None:
        """Initialise the help screen.

        Args:
            help_for: The screen to show the help for.
        """
        super().__init__()
        self._context_help = "\n\n".join(
            cleandoc(getattr(helper, "CONTEXT_HELP"))
            for helper in reversed(
                (
                    help_for.focused if help_for.focused is not None else help_for
                ).ancestors_with_self
            )
            if hasattr(helper, "CONTEXT_HELP")
        ).strip()

    def compose(self) -> ComposeResult:
        """Compose the layout of the help screen."""
        with Vertical() as help_screen:
            help_screen.border_title = "Help"
            with VerticalScroll():
                yield Markdown(
                    HELP.replace("[EOL]", "  ").format(context_help=self._context_help)
                )
            with Center():
                yield Button("Okay [dim]\\[Esc]")

    @on(Button.Pressed)
    def action_close(self) -> None:
        """Close the help screen."""
        self.dismiss(None)

    @on(Markdown.LinkClicked)
    def visit(self, event: Markdown.LinkClicked) -> None:
        """Visit any link clicked in the help."""
        open_url(event.href)


### help.py ends here
