import django_saml2_auth
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin"), name="index"),
    path("saml/", include('django_saml2_auth.urls')),
    path("login/", django_saml2_auth.views.signin, name="saml-login"),
    path("logout/", django_saml2_auth.views.signout, name="saml-logout"),
    path("admin/login/", RedirectView.as_view(url="/login"), name="login-redirect"),
    path("admin/logout/", RedirectView.as_view(url="/logout"), name="logout-redirect"),
    path("admin-login/", admin.site.login, name="admin-login"),
    path("frontoffice/", include("frontoffice.urls")),
    path("admin/", admin.site.urls),
]
