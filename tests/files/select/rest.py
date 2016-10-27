from wq.db import rest
from .models import Select


rest.router.register_model(
    Select,
    fields="__all__",
)
