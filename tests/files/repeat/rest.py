from wq.db import rest
from .models import Repeat
from .serializers import RepeatSerializer


rest.router.register(
    Repeat,
    serializer=RepeatSerializer,
    fields="__all__",
    cache="first_page",
    background_sync=True,
)
