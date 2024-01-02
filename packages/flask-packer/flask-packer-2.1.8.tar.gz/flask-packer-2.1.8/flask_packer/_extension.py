import difflib
import hashlib
import os
from typing import Generator

from bs4 import BeautifulSoup
from flask import Flask, Blueprint
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Const
from jinja2.parser import Parser
from jinja2.runtime import Macro

from flask_packer._errors import FileTypeUnsupported, FileNotFound
from flask_packer.tags import CssTag, JsTag


class Config(dict):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.update(**kwargs)

    def __getattr__(self, key: str) -> any:
        return self[key]


class Pack:
    def __init__(
        self, url: str, extension: str, async_: bool = False, defer: bool = False
    ) -> None:
        self.url = url
        self.extension = extension
        self.async_ = async_
        self.defer = defer


class Line:
    def __init__(self) -> None:
        self.url = None
        self.mimetype = None
        self.content = None


class FlaskPackerExtension(Extension):
    tags = {"pack"}
    extensions = {"css", "js"}
    encoding = "utf-8"

    def __init__(self, *args, **kwargs) -> None:
        super(FlaskPackerExtension, self).__init__(*args, **kwargs)
        self.config = Config()

    def parse(self, parser: Parser) -> CallBlock:
        # Update config with jinja environment
        self.config.update(
            **{
                k: getattr(self.environment, k)
                for k in dir(self.environment)
                if k.startswith("pack_")
            }
        )

        # Save lineno
        lineno = next(parser.stream).lineno

        # Parse extension (1st arg)
        arg1 = parser.parse_expression()

        # Parse mode (2nd arg)
        if parser.stream.skip_if("comma"):
            if parser.stream.skip_if("name:mode"):
                parser.stream.skip(1)
            arg2 = parser.parse_expression()
        else:
            arg2 = Const(None)

        # Create callblock
        body = parser.parse_statements(("name:endpack",), drop_needle=True)
        callblock = CallBlock(self.call_method("pack", [arg1, arg2]), [], [], body)
        callblock.set_lineno(lineno)
        return callblock

    def pack(self, extension: str, mode: str | None, caller: Macro) -> str:
        """Pack multiple lines of code into one."""

        # Lower extension
        extension = extension.lower()
        if extension not in self.extensions:
            raise FileTypeUnsupported

        # Generate html hash
        html = caller()
        html_hash = self.make_hash(html)

        # Create Pack object
        path = os.path.join(self.config.pack_output_dir, f"{html_hash}.{extension}")
        url = os.path.join(self.config.pack_output_url, os.path.basename(path))
        async_, defer = mode == "async", mode == "defer"
        pack = Pack(url, extension, async_, defer)

        # Try to fetch cached content
        if os.path.exists(path):
            return self.render_element(pack)

        # Create static dirs
        if not os.path.exists(self.config.pack_output_dir):
            os.makedirs(self.config.pack_output_dir)

        # Combine compiled content from lines
        compiled = ""
        for line in self.find_lines(BeautifulSoup(html, "html.parser")):
            line_path = self.find_path_by_url(line.url)
            content = open(line_path, "r", encoding=self.encoding).read()
            compiled += f"{self.config.pack_packers[line.mimetype].compile(content)}\n"

        # Write and render element
        with open(path, "w", encoding=self.encoding) as file:
            file.write(compiled)
        return self.render_element(pack)

    def make_hash(self, html: str) -> str:
        """Make a hash from HTML content (a string)."""

        return hashlib.md5(html.encode(self.encoding)).hexdigest()

    @staticmethod
    def find_lines(soup: BeautifulSoup) -> Generator[Line, None, None]:
        """Find all processable tags in a soup and yield Line objects."""

        for tag in soup.find_all(["link", "style", "script"]):
            line = Line()
            line.content = tag.string
            url = tag.get("src") or tag.get("href")
            if url is None:
                continue
            line.url = url
            if tag.name in ["style", "link"]:
                line.mimetype = "text/css"
            elif tag.name in ["script"]:
                line.mimetype = "text/javascript"
            else:
                continue
            yield line

    def find_path_by_url(self, url: str = None) -> str:
        """Find an absolute path by providing a (partial) URL."""

        # Generate list with blueprints
        blueprints: list[Flask | Blueprint] = []
        if self.config.pack_app.has_static_folder:
            blueprints.append(self.config.pack_app)
        blueprints.extend(
            [x for x in self.config.pack_app.blueprints.values() if x.has_static_folder]
        )

        # Match basename with static files
        # Generate a list of absolute paths
        # List will contain multiple results if files with the same name exists
        basename = os.path.basename(url)
        abs_paths = []
        for bp in blueprints:
            for dir_, _, files in os.walk(bp.static_folder):
                for file in files:
                    if file == basename:
                        abs_paths.append(os.path.join(dir_, file))

        # Return if there is one match
        if len(abs_paths) == 1:
            return abs_paths[0]

        # Find closest match
        match, match_ratio = None, -1
        for abs_path in abs_paths:
            ratio = difflib.SequenceMatcher(None, abs_path, url).ratio()
            if url in abs_path:
                ratio += 1
            if ratio > match_ratio:
                match, match_ratio = abs_path, ratio
        if match is not None:
            return match

        # Raise if there are no matches
        raise FileNotFound

    @staticmethod
    def render_element(pack: Pack) -> str:
        """Render an HTML element from a Pack object."""

        match pack.extension:
            case "css":
                return str(CssTag(pack.url))
            case "js":
                return str(JsTag(pack.url, pack.async_, pack.defer))
            case _:
                raise FileTypeUnsupported
