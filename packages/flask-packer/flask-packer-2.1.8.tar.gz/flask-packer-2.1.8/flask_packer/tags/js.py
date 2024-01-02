from rjsmin import jsmin


class JsTag:
    TEMPLATE = f'<script %(async)s %(defer)s type=%(type)s src="%(url)s"></script>'

    def __init__(self, url: str, async_: bool = False, defer: bool = False) -> None:
        self.url = url
        self.async_ = "async" if async_ else ""
        self.defer = "defer" if defer else ""

    def __str__(self) -> str:
        return self.TEMPLATE % {
            "url": self.url,
            "type": "text/javascript",
            "async": self.async_,
            "defer": self.defer,
        }


class JsPacker(object):
    @classmethod
    def compile(cls, js: str, *args, **kwargs) -> str:
        return jsmin(js)
