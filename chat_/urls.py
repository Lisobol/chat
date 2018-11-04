"""chat_ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from chat_ import settings
from core.views import LoginPageView, ChatPageView, MessageView, logout_view, registration, MessagesView, \
    upload_file, upload_pic

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LoginPageView.as_view(), name='login'),
    url(r'^chat/$', ChatPageView.as_view(), name='chat'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^message/$', MessageView.as_view(), name='message'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'messages/$', MessagesView.as_view(), name='messages'),
    # url(r'^upload/$',UploadFileView.as_view(), name = 'upload'),
    url(r'^upload/$',upload_file,name='upload'),
    url(r'^user_profile/$',upload_pic,name='user_profile')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)