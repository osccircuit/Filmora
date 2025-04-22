from django.urls import path
from subscription import views

app_name = 'subscription'

urlpatterns = [
    path('subscription-registration/', views.OrderSubscriptionView.as_view(), name='subscription_registration'),
    path('subscription-pay/', views.PaySubscription.as_view(), name='subscription_pay'),
    path('subscription-variant/', views.VariantSubscriptionView.as_view(), name='subscription_variant'),
]
