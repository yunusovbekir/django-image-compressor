from django.views.generic import CreateView
from .models import ExampleModel
from .forms import ExampleForm


class ExampleCreateView(CreateView):
    model = ExampleModel
    form_class = ExampleForm
