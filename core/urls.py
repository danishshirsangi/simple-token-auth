from django.urls import path
from . import views


urlpatterns = [
    path('',views.home_view, name = "Homepage"),
    path('add/',views.add_view, name = "Addview"),
    path('api/users/',views.users_api_view,name="users-api-view"),
    path('api/details/<str:btype>/',views.user_donordonee_api,name="users-api-view"),
    path('api/users/token/',views.generate_token,name="token-generate")
]