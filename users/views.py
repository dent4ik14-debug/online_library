from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from book_catalog.models import Basket
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')


class CustomRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context