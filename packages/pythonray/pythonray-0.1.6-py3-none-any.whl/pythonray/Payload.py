import platform
from inspect import getframeinfo, stack

class Payload:

    VERSION = "0.1.6"

    @staticmethod
    def get_origin():
        info = getframeinfo(stack()[-2][0])
        return {
            # "function_name": getframeinfo(stack()[-2][0]).function,
            "file": info[0],
            "line_number": info[1],
            "hostname": platform.node(),
        }

    def sendable(self):
        payloads = self
        # If payloads is not a list, make it a list
        if not isinstance(payloads, list):
            payloads = [payloads]
        python_version = platform.python_version()
        # Replace first . with 0
        python_version_id = python_version.replace(".", "0", 1)
        python_version_id = int(python_version_id.replace(".", ""))
        return {
            "payloads": [p.__dict__ for p in payloads],
            "meta" : {
                "python_version": python_version,
                "python_version_id": python_version_id,
                "python_ray_version": self.VERSION,
                "project_name" : ""
            }
        }

    def __init__(self, type, content, content_name = "content", label = None):
        self.type = type
        if isinstance(content, str):
            self.content = {
                content_name: content
            }
        else:
            self.content = content
        if label:
            self.content["label"] = label
        self.origin = Payload.get_origin()

    def __str__(self):
        return f"Payload(type={self.type}, content={self.content})"

class ConfettiPayload(Payload):
    def __init__(self):
        super().__init__(type="confetti", content=None)

class ColorPayload(Payload):
    # Define constant for available colors
    COLORS = ["green", "orange", "red", "purple", "blue", "gray"]
    def __init__(self, color):
        if color not in self.COLORS:
            raise Exception(f"Color {color} is not a valid color. Please use one of the following: {self.COLORS}")
        self.color = color
        super().__init__(type="color", content=color, content_name="color")

class ScreenColorPayload(Payload):
    # Define constant for available colors
    COLORS = ["green", "orange", "red", "purple", "blue", "gray"]
    def __init__(self, color):
        if color not in self.COLORS:
            raise Exception(f"Color {color} is not a valid color. Please use one of the following: {self.COLORS}")
        self.color = color
        super().__init__(type="screen_color", content=color, content_name="color")

class ClearAllPayload(Payload):
    def __init__(self):
        super().__init__(type="clear_all", content=None)

class HtmlPayload(Payload):
    def __init__(self, html):
        self.content = {
            'content': html,
            'label': 'HTML',
        }
        super().__init__(type="custom", content=self.content)

class BooleanPayload(Payload):
    def __init__(self, boolean):
        super().__init__(type="custom", content={
            'content': boolean,
            'label': 'Boolean',
        })

class NewScrenPayload(Payload):
    def __init__(self, name):
        super().__init__(type="new_screen", content={
            'name' : name or ""
        })


class HidePayload(Payload):
    def __init__(self):
        super().__init__(type="hide", content={})

class HideAppPayload(Payload):
    def __init__(self):
        super().__init__(type="hide_app", content={})
class ShowAppPayload(Payload):
    def __init__(self):
        super().__init__(type="show_app", content={})

class RemovePayload(Payload):
    def __init__(self):
        super().__init__(type="remove", content={})