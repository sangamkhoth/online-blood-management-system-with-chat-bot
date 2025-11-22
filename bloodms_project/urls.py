from django.contrib import admin
from django.urls import path, include
from chatbot.views import chat_page, chatbot_api
from .views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('api/', include('api.urls')),

    # Chatbot API
    path('api/chat/', chatbot_api, name='chatbot_api'),

    # Chat UI
    path('chatbot/', chat_page, name='chat_page'),
]
