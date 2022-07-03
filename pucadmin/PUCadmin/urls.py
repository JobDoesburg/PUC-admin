from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin"), name="index"),
    path("taggit/", include("taggit_selectize.urls")),
    path("sso/<idp_slug>/", include("sp.urls")),
    path(
        "login/",
        RedirectView.as_view(
            url="/sso/science_puc/login/" if not settings.DEBUG else "/admin-login"
        ),
        name="login",
    ),
    path(
        "logout/",
        RedirectView.as_view(
            url="/sso/science_puc/logout/" if not settings.DEBUG else "/admin-logout"
        ),
        name="logout",
    ),
    path("admin/login/", RedirectView.as_view(url="/login"), name="login-redirect"),
    path("admin/logout/", RedirectView.as_view(url="/logout"), name="logout-redirect"),
    path("admin-login/", admin.site.login, name="admin-login"),
    path("admin-logout/", admin.site.logout, name="admin-logout"),
    path("admin/", admin.site.urls),
    path("frontoffice/", include("frontoffice.urls")),
    path("secondments-frontoffice/", include("secondments_frontoffice.urls")),
]
