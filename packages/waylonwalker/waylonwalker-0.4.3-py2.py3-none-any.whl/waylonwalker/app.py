import webbrowser

from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.css.query import NoMatches
from textual.message import Message
from textual.widgets import Footer, Header, Static, Markdown
import httpx

LINKS = [
    ("home", "https://waylonwalker.com/"),
    ("blog", "https://waylonwalker.com/archive/"),
    ("YouTube", "https://youtube.com/waylonwalker"),
    ("Twitch", "https://www.twitch.tv/waylonwalker"),
    ("Twitter", "https://twitter.com/_waylonwalker"),
    ("Dev.to", "https://dev.to/waylonwalker"),
    ("LinkedIn", "https://www.linkedin.com/in/waylonwalker/"),
]

THOUGHTS = [
    (
        thought["title"][:50],
        f'https://thoughts.waylonwalker.com/post/{thought["id"]}',
        thought,
    )
    for thought in httpx.get(
        "https://thoughts.waylonwalker.com/posts/waylonwalker/?page_size=99999"
    ).json()
]


class Post(Markdown):
    def __init__(self, post):
        super().__init__(post[2]["message"])
        self.post = post[2]
        self.set_message()

    def set_post(self, index):
        self.post = THOUGHTS[index][2]
        self.set_message()

    def set_message(self):
        self.message = (
            f'# {self.post["title"]}\n{self.post["link"]}\n\n{self.post["message"]}'
        )
        self.update(self.message)


class Link(Static):
    def __init__(self, title, url, thought=None):
        super().__init__(title)
        self.title = title
        self.url = url

    class ClearActive(Message):
        ...

    def on_click(self):
        webbrowser.open(self.url)

    def on_enter(self):
        self.add_class("active")

    async def on_leave(self):
        self.remove_class("active")
        # await self.emit(self.ClearActive(self))


class WaylonWalker(App):
    CSS = """
    Link {
        background: $primary-background;
        margin: 1;
        padding: 1;
    }
    Static.active {
        background: $accent;
    }

    Static:focus {
        background: $accent;
    }

    #about {

        border: round white;
        color: $text-muted;
            }
    .mt-1 {
        margin-top: 1;
    }
    .mt-2 {
        margin-top: 2;
    }
    .mt-3 {
        margin-top: 3;
    }

    .my-1 {
        margin-top: 1;
        margin-bottom: 1;
    }
    .py-1 {
        padding-top: 1;
        padding-bottom: 1;
    }
    .my-2 {
        margin-top: 2;
        margin-bottom: 2;
    }
    .py-2 {
        padding-top: 2;
        padding-bottom: 2;
    }
    .my-3 {
        margin-top: 3;
        margin-bottom: 3;
    }

    .max-w-3xl {
        max-width: 80;
    }

    .font-bold {
        text-style: bold;
    }

    .bg-blue {
        background: $accent;
    }

    .top-0 {
        dock: top;
    }

    .border-1 {
        border: wide black;
    }

    .border-2 {
        border: thick black;
    }

    .text-center {
        text-align: center;
    }

    .center {
        align: center middle;
        content-align: center middle;
    }

    #posts {
        width: 1fr;
        height: 1fr;
        border: solid white;
    }
    #links {
        width: 1fr;
        height: 1fr;
        border: solid white;
    }

    #content-grid {
    layout: grid;
    grid-size: 3 1;
    grid-rows: 1fr;
    grid-columns: 20 1fr 1fr;
    grid-gutter: 1;

    }

    #content {
     layout: grid;
    grid-size: 1 2;
    grid-rows: 8 1fr;

    }

    #post {
            margin-top: 0;
            height: 100%;
            }




    """
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("d", "toggle_dark", "Dark Mode"),
        ("q", "quit", "Quit"),
        ("j", "next", "Next"),
        ("down", "next", "Next"),
        ("k", "previous", "Prev"),
        ("up", "previous", "Prev"),
        ("h", "left", "Left"),
        ("left", "left", "Left"),
        ("l", "right", "Right"),
        ("u", "page_up", "Page Up"),
        ("d", "page_down", "Page Down"),
        ("right", "right", "Right"),
        ("enter", "open", "Open Link"),
        ("space", "open", "Open Link"),
    ]

    def on_mount(self):
        active = self.query("Link").first()
        active.focus()
        active.add_class("active")

    def action_next(self):
        self.select(1)

    def action_previous(self):
        self.select(-1)

    def action_page_down(self):
        self.select(5)

    def action_page_up(self):
        self.select(-5)

    def action_left(self):
        links = self.query("Link")
        try:
            active = self.query_one(".active")
        except NoMatches:
            links[0].add_class("active")
            return
        active_index = links.nodes.index(active)
        if active_index > len(LINKS):
            self.select(active_index - len(LINKS), absolute=True)

    def action_right(self):
        links = self.query("Link")
        try:
            active = self.query_one(".active")
        except NoMatches:
            links[0].add_class("active")
            return
        active_index = links.nodes.index(active)
        if active_index < len(LINKS):
            self.select(len(LINKS) + active_index, absolute=True)

    def select(self, n=1, absolute=False):
        links = self.query("Link")
        post = self.query("Post").first()
        try:
            active = self.query_one(".active")
        except NoMatches:
            links[0].add_class("active")
            return
        active_index = links.nodes.index(active)
        if absolute:
            next_index = n
        else:
            next_index = active_index + n
        if next_index >= len(links):
            next_index = 0
        elif next_index < 0:
            next_index = len(links) - 1

        active.remove_class("active")
        links[next_index].add_class("active")
        active = self.query_one(".active")
        active.scroll_visible()
        if next_index > len(LINKS) - 1:
            post.set_post(next_index - len(LINKS))

    def on_link_clear_active(self):
        for node in self.query(".active").nodes:
            node.remove_class("active")

    async def action_open(self) -> None:
        webbrowser.open(self.query_one(".active").url)

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Container(
                Static(
                    "Hey, Im Waylon.  Husband, Father of two beautiful children, Senior Python Developer currently working in the Data Engineering platform space. I am a continuous learner, and share my learning in public.",
                    id="about",
                    classes="max-w-3xl my-1 py-1",
                ),
                id="about-container",
                classes="center",
            ),
            Container(
                ScrollableContainer(
                    Static(
                        "Social Links",
                        classes="top-0 py-1 text-center border-1 bg-blue font-bold",
                    ),
                    *[Link(*link) for link in LINKS],
                    id="links",
                ),
                ScrollableContainer(
                    Static(
                        "Thoughts from thoughts.waylonwalker.com",
                        classes="top-0 py-1 text-center border-1 bg-blue font-bold",
                    ),
                    *[Link(*link) for link in THOUGHTS],
                    id="posts",
                ),
                ScrollableContainer(
                    Post(THOUGHTS[0]),
                    id="post",
                ),
                id="content-grid",
            ),
            id="content",
        )
        yield Footer()


if __name__ == "__main__":
    import os
    import sys

    from textual.features import parse_features

    # this works, but putting it behind argparse, click, or typer would be much
    # better

    dev = "--dev" in sys.argv

    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if dev:
        features.add("debug")
        features.add("devtools")

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    WaylonWalker.run(title="Waylon Walker")
