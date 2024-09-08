from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My Library Admin API",
        default_version='v1',
        description="the api that is used by the admin alone to update the library and view users activity",
        terms_of_service="",
        contact=openapi.Contact(email="oludarenathaniel@gmail.com"),
        license=openapi.License(name="Nathan Yinka"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", include("api.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
