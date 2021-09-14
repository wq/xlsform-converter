import data_wizard
from .models import Repeat
from .serializers import RepeatSerializer


data_wizard.register("repeat", RepeatSerializer)
