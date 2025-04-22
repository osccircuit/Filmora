from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "subscription/subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление подписки"
        return context


class PaySubscription(LoginRequiredMixin, View):

    def post(self, request):
        subscription_level = request.COOKIES.get('subscription_level')
        response = JsonResponse({
            "message": f"Подписка {subscription_level} успешно оплачена вы будете перенаправлены на главную страницу через 5 секунд",
            "redirect_url": reverse("library:films"),
        })
        response.delete_cookie('subscription_level')
        return response

class VariantSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "subscription/variant_sub.html"
    sub_level = ''

    def post(self, request, *args, **kwargs):
        self.sub_level = request.POST.get('level_sub')
        response = JsonResponse({
            "redirect_url": reverse("subscription:subscription_registration"),
        })
        response.set_cookie(
           key="subscription_level",    # Название куки
            value=self.sub_level,       # Значение
            max_age=3600,               # Время жизни (1 час)
            samesite='Lax'
        )
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Выбор подписки"
        return context

