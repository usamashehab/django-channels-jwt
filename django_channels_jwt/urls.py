from django.urls import path
from .views import AsgiValidateTokenView


urlpatterns = [
    path("auth_for_ws_connection/", AsgiValidateTokenView.as_view())
]
