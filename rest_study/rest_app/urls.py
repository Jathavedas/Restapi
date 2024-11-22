from django.urls import path,include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'person', views.PersonViewSet, basename='person')

urlpatterns = [
    path('',include(router.urls)),
    path('index/',views.index),
    path('person/',views.person),
    path('classperson/',views.PersonClass.as_view()),
    path('register/',views.RegisterApi.as_view()),
    path('login/',views.LoginApi.as_view()),
    path('classperson/',views.ClassPerson.as_view())
]