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
        subscription_level = request.POST.get("level")
        redirect_url = reverse("library:films")
        response = {
            "message": f"Подписка {subscription_level} успешно оплачена вы будете перенаправлены на главную страницу через 5 секунд",
            "redirect_url": redirect_url,
        }
        return JsonResponse(response)
