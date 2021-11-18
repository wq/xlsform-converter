from wq.db import rest
from .models import Nestedfk
from .serializers import NestedfkSerializer


rest.router.register_model(
    Nestedfk,
    serializer=NestedfkSerializer,
    fields="__all__",
    cache="first_page",
    background_sync=True,
)
