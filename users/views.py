from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from book_catalog.models import Basket
# Create your views here.

# Генератор токенів підтвердження
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

email_verification_token = EmailVerificationTokenGenerator()


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')


class CustomRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_verification_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Користувач неактивний до підтвердження email
        user.save()

        # Формування даних для листа
        current_site = get_current_site(self.request)
        mail_subject = 'Підтвердження реєстрації'
        
        # Рендеримо HTML-шаблон
        html_content = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        })
        
        # Створюємо текстову версію листа (для поштових клієнтів без підтримки HTML)
        text_content = strip_tags(html_content)

        # Створюємо мультиформатний лист
        msg = EmailMultiAlternatives(
            subject=mail_subject,
            body=text_content,
            from_email=None,  # Використовує DEFAULT_FROM_EMAIL із settings.py
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")  # Підключаємо HTML-версію
        msg.send()

        return super().form_valid(form)


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/activation_success.html')
        else:
            return render(request, 'users/activation_invalid.html')


class EmailVerificationSentView(TemplateView):
    template_name = 'users/email_verification_sent.html'


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