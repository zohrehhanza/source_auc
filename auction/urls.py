from django.conf.urls import url,include
from django.contrib import admin
from main import views
#from profiles import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'', include('main.urls' )),
   # url(r'', include('chat.urls',namespace='chat')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
