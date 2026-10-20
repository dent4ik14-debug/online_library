import os
import requests
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from book_catalog.models import Basket  # замініть імпорт на ваш модуль із Basket
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:payment_success')

    def get_initial(self):
        # Автоматично підставляємо ім'я, прізвище та email з профілю користувача
        initial = super().get_initial()
        user = self.request.user
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо кошик у контекст для виводу загальної суми в шаблоні
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        # 1. Прив'язуємо замовлення до поточного користувача
        form.instance.user = self.request.user
        order = form.save()

        # 2. Переносимо товари з Basket у OrderItem (або в basket_history, якщо у вас JSONField)
        baskets = Basket.objects.filter(user=self.request.user)
        for basket in baskets:
            OrderItem.objects.create(
                order=order,
                book=basket.book,
                price=basket.book.price,
                quantity=basket.quantity
            )
        
        # 3. Очищаємо кошик користувача
        baskets.delete()

        # 4. Перенаправляємо на ініціалізацію оплати Monobank
        return redirect('orders:create_payment', order_id=order.id)


def create_payment(request, order_id):
    """
    Формує запит до Monobank та перенаправляє на сторінку еквайрингу
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    url = "https://api.monobank.ua/api/merchant/invoice/create"
    headers = {
        "X-Token": os.getenv('MONO_API_TOKEN'),
        "Content-Type": "application/json"
    }

    # Розрахунок суми у копійках (наприклад, 150 грн -> 15000)
    # Зверніть увагу: скоригуйте за вашою моделлю (наприклад, order.total_sum)
    total_cost = sum(item.price * item.quantity for item in order.items.all())
    amount_in_cents = int(total_cost * 100)

    payload = {
        "amount": amount_in_cents,
        "ccy": 980,  # UAH
        "merchantPaymInfo": {
            "reference": str(order.id),
            "destination": f"Оплата замовлення №{order.id}"
        },
        "redirectUrl": request.build_absolute_uri(reverse('orders:payment_success')),
        "webHookUrl": request.build_absolute_uri(reverse('orders:mono_webhook'))
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return redirect(data['pageUrl'])
    else:
        return redirect('orders:payment_failed')


def payment_success(request):
    return render(request, 'orders/payment_success.html')


def payment_failed(request):
    return render(request, 'orders/payment_failed.html')

@csrf_exempt
def mono_webhook(request):
    """
    Приймає сповіщення від Monobank про зміну стану платежу
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Якщо платіж успішний
            if data.get('status') == 'success':
                order_id = data.get('merchantPaymInfo', {}).get('reference')
                if order_id:
                    order = Order.objects.get(id=order_id)
                    order.status = Order.PAID  # Або за вашим статусом (наприклад, 1)
                    order.save()

            return HttpResponse(status=200)
        except Exception:
            return HttpResponse(status=400)

    return HttpResponse(status=405)