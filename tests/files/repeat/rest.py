from wq.db import rest
from .models import Repeat
from .serializers import RepeatSerializer


rest.router.register_model(
    Repeat,
    serializer=RepeatSerializer,
)
