from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


BUTTONS = [
    ("Send",       (0.10, 0.40, 0.95, 1)),
    ("File",       (0.10, 0.65, 0.25, 1)),
    ("Copy MW",    (0.55, 0.25, 0.80, 1)),
    ("PC_Android", (0.00, 0.65, 0.70, 1)),
    ("Setup",      (0.95, 0.48, 0.08, 1)),
    ("Favorites",  (0.90, 0.20, 0.48, 1)),
    ("Forward",    (0.95, 0.75, 0.10, 1)),
    ("Back",       (0.85, 0.12, 0.12, 1)),
]


def create_toolbar(callback):
    toolbar = BoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=dp(42),
        spacing=dp(1)
    )

    buttons = {}

    # نمایش بصری از راست به چپ:
    # Send, File, Copy MW, PC_Android,
    # Setup, Favorites, Forward, Back

    for name, color in reversed(BUTTONS):
        button = Button(
            text=name,
            font_size=dp(9),
            size_hint_x=1,
            background_normal="",
            background_color=color,
            color=(1, 1, 1, 1)
        )

        button.original_color = color

        button.bind(
            on_release=lambda instance, key=name:
                callback(key)
        )

        buttons[name] = button
        toolbar.add_widget(button)

    return toolbar, buttons
