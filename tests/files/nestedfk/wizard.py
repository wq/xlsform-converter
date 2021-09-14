import data_wizard
from .models import Nestedfk
from .serializers import NestedfkSerializer


data_wizard.register("nestedfk", NestedfkSerializer)
