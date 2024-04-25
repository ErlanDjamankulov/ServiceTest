from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('select-topic/', select_topic, name='select_topic'),
    path('start-test/<int:topic_id>/', start_test, name='start_test'),
    path('show-question/', show_question, name='show_question'),
    path('handle-answer/', handle_answer, name='handle_answer'),
    path('show-result/', show_result, name='show_result'),
]