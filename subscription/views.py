from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class OrderSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "subscription/subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление подписки"
        return context

