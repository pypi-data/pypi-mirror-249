import os

from flask import Flask

from flask_packer._errors import NotInitialized
from flask_packer.tags.css import CssPacker
from flask_packer.tags.js import JsPacker


class FlaskPacker:
    output = "sdist"

    def __init__(self, app: Flask = None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.jinja_env.add_extension("flask_packer._extension.FlaskPackerExtension")
        app.jinja_env.pack_app = app
        app.jinja_env.pack_output_dir = os.path.join(app.static_folder, self.output)
        app.jinja_env.pack_output_url = os.path.join(app.static_url_path, self.output)
        app.jinja_env.pack_packers = {
            "text/css": CssPacker,
            "text/javascript": JsPacker,
        }

    def set_packer(self, mimetype: str, packer: any) -> None:
        if not hasattr(self, "app") or self.app is None:
            raise NotInitialized
        self.app.jinja_env.pack_packers[mimetype] = packer
