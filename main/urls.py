from django.urls import path
from main.views import show_main, create_product_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, view_profile, edit_dashboard, delete_account, logout_user
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product-entry', create_product_entry, name='create_product_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-dashboard', edit_dashboard, name='edit_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('profile/', view_profile, name='view_profile'),
    path('delete-account/', delete_account, name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)