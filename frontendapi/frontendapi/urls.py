from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My Library Frontend API",
        default_version='v1',
        description="This api is used at the frontend for users to interact with the library",
        terms_of_service="",
        contact=openapi.Contact(email="oludarenathaniel@gmail.com"),
        license=openapi.License(name="Nathan Yinka"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/",include("api.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
]
