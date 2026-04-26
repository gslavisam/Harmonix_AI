from __future__ import annotations

import reflex as rx

from harmonix.ui.components import app_page


app = rx.App(theme=rx.theme(accent_color="amber", appearance="dark", gray_color="slate"))
app.add_page(app_page, route="/", title="Harmonix AI")