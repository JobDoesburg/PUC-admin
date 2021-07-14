import django_saml2_auth
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("saml/", include("django_saml2_auth.urls")),
    path("login/", django_saml2_auth.views.signin, name="saml-login"),
    path("logout/", django_saml2_auth.views.signout, name="saml-logout"),
    path("admin-login/", admin.site.login, name="admin-login"),
    path("frontoffice/", include("frontoffice.urls")),
    path("", admin.site.urls),
]
