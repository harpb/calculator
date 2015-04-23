from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^evaluate/$', views.EvaluateExpressionView.as_view(), name='evaluate'),
]
