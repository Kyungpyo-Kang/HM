from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import DesignAssistant.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',DesignAssistant.views.main_view, name='index'),
    path('transfer',DesignAssistant.views.transfer_view, name='transfer'),
    path('result',DesignAssistant.views.result_view, name='result'),
    path('history',DesignAssistant.views.history_view, name='history'),
    path('setseq',DesignAssistant.views.setseq, name='setseq'),
    path('delete',DesignAssistant.views.delete_history, name='delete'),
    path('get_images',DesignAssistant.views.get_images, name='get_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)