
from django.urls import path
from .views import CreateContactView, ContactDetailView, LoginView, RegisterUsers
urlpatterns = [
   
    path('contacts/', CreateContactView.as_view(), name="contacts-all"),
    path('contacts/(?P<name>[\w\-]+)/$', ContactDetailView.as_view(), name="contact-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]