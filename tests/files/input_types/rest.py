from wq.db import rest
from .models import InputTypes


rest.router.register(
    InputTypes,
    fields="__all__",
    cache="first_page",
    background_sync=True,
    map=[
        {
            "mode": "list",
            "autoLayers": True,
            "layers": [],
        },
        {
            "mode": "detail",
            "autoLayers": True,
            "layers": [],
        },
        {
            "mode": "edit",
            "autoLayers": True,
            "layers": [],
        },
    ],
)
