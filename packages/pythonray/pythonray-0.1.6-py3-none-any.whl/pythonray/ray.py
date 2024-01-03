import uuid
import requests
from pythonray.Payload import *

class Ray:
    # Contstants
    PORT = 23517
    HOST = "localhost"

    def __init__(self, host=None, port=None, id=None):
        self.host = host if host else Ray.HOST
        self.port = port if port else Ray.PORT
        self.id = id if id else str(uuid.uuid4())
        self.payload = None

    def __str__(self):
        return f"Ray(host={self.host}, port={self.port}, id={self.id})"

    def send(self, data = None):
        if data is not None:
            if isinstance(data, Payload):
                self.payload = data
            else:
                if isinstance(data, bool):
                    self.payload = BooleanPayload(data)
                else:
                    if isinstance(data, str):
                        self.payload = Payload(type="custom", content=data)
                    else:
                        self.payload = Payload(type="custom", content=str(data))
        if self.payload is not None:
            payload = self.payload.sendable()
            payload["uuid"] = self.id
            requests.post(f"http://{Ray.HOST}:{Ray.PORT}/", json=payload)
            return self
        else:
            raise Exception("No data to send, and no payload set")

    ### COLORS
    def color(self, color):
        return self.send(ColorPayload(color))

    def green(self): return self.color("green")
    def orange(self): return self.color("orange")
    def red(self): return self.color("red")
    def purple(self): return self.color("purple")
    def blue(self): return self.color("blue")
    def gray(self): return self.color("gray")

    def screen_color(self, color):
        return self.send(ScreenColorPayload(color))

    def screen_green(self): return self.screen_color("green")
    def screen_orange(self): return self.screen_color("orange")
    def screen_red(self): return self.screen_color("red")
    def screen_purple(self): return self.screen_color("purple")
    def screen_blue(self): return self.screen_color("blue")
    def screen_gray(self): return self.screen_color("gray")
    def screen_color_green(self): return self.screen_color("green")
    def screen_color_orange(self): return self.screen_color("orange")
    def screen_color_red(self): return self.screen_color("red")
    def screen_color_purple(self): return self.screen_color("purple")
    def screen_color_blue(self): return self.screen_color("blue")
    def screen_color_gray(self): return self.screen_color("gray")

    # Methods
    def html(self, html):
        return self.send(HtmlPayload(html))

    ### Utilities
    # Clear all
    def clear(self):
        return self.send(ClearAllPayload())
    def clear_all(self):
        return self.clear()
    # Hide or Show App
    def hide_app(self):
        return self.send(HideAppPayload())
    def show_app(self):
        return self.send(ShowAppPayload())

    # Hide item
    def hide(self):
        return self.send(HidePayload())
    # Make new screen
    def new_screen(self, name = None):
        return self.send(NewScrenPayload(name=name))
    def remove(self):
        return self.send(RemovePayload())



    ### Fun Utilities
    def confetti( self):
        return self.send(ConfettiPayload())
    def charles(self):
        return self.send("'🎶 🎹 🎷 🕺'")
    def ban(self):
        return self.send("🕶️")


def ray(data = None):
    if data is None:
        return Ray()
    return Ray().send(data)
