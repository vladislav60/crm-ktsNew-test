"""ktscrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin

# №4 нужно импортировать для того что бы приложения могли быть не зависимыми
from django.urls import path, include

from dogovornoy.views import pageNotFound
from ktscrm import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # №3 регистрируем ссылку на главную страницу
    path('', include('dogovornoy.urls')),
]

#11 Эмуляция рабочего сервера для фото
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#8 Добавляем обработчик 404 измененный далее в файле dogovornoy-views.py
handler404 = pageNotFound