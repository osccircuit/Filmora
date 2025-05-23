from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
import datetime
# from datetime import datetime, timedelta


class OrderSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "subscription/subscription.html"

    def dispatch(self, request, *args, **kwargs):
        access_status = request.session.get('allow_access')
        if not access_status:
            return HttpResponseRedirect(reverse("library:films"))
        del self.request.session['allow_access']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление подписки"
        return context


class PaySubscription(LoginRequiredMixin, View):

    def post(self, request):
        subscription_level = request.session.get('pending_sub')
        
        error_response = {"error": "Такого варианта подписки не существует.",
                                          "redirect_url": reverse("library:films")}
                
        if subscription_level in User.TypeOfSub.get_list_choices():
            del self.request.session['pending_sub']
            timedelta = User.TypeOfSub.get_deltatime_for_sub(subscription_level)
            if timedelta is None:
                return JsonResponse(error_response, status=400)
            user_new_sub = request.user
            user_new_sub.type_of_sub = subscription_level
            user_new_sub.date_to_pay = datetime.datetime.now().date() + datetime.timedelta(days=timedelta)
            user_new_sub.save()
            response = {
                "message": f"Подписка {subscription_level} успешно оплачена вы будете перенаправлены на главную страницу через 5 секунд",
                "redirect_url": reverse("library:films"),
            }
            return JsonResponse(response)
        return JsonResponse(error_response, status=400)
                

class VariantSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "subscription/variant_sub.html"

    def post(self, request, *args, **kwargs):
        sub_level = request.POST.get('level_sub')
        self.request.session['pending_sub'] = sub_level
        self.request.session['allow_access'] = True 
        response = {
            "redirect_url": reverse("subscription:subscription_registration"),
        }
        return JsonResponse(response)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Выбор подписки"
        return context

