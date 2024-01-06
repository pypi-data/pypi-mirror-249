"""Stream from your website."""

import web

app = web.application(__name__, prefix="live")


@app.control("")
class Live:
    """Live stream and chat."""

    def get(self):
        """Return both stream and chat."""
        return app.view.index()


@app.control("stream")
class Stream:
    """Stream to consumers (listeners/viewers)."""

    def get(self):
        """Return a live stream (RTMP)."""
        return app.view.stream()


@app.control("chat")
class Chat:
    """Chat with guests."""

    def get(self):
        """Return a video chat ([Web]RTC)."""
        return app.view.chat()
