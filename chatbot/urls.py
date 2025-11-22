from django.urls import path
from .views import chat_page, chatbot_api

urlpatterns = [
    path('', chat_page, name='chat_page'),  # ✅ main chatbot page
    path('api/', chatbot_api, name='chatbot_api'),
]
