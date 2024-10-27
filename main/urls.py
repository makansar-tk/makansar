from django.urls import path, include
from main.views import show_main, create_product_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, edit_dashboard, get_makanan_by_kategori, get_makanan_detail

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product-entry/', create_product_entry, name='create_product_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-dashboard/', edit_dashboard, name='edit_dashboard'),
    path('get_makanan_by_kategori/', get_makanan_by_kategori, name='get_makanan_by_kategori'),
    path('get_makanan_detail/', get_makanan_detail, name='get_makanan_detail'),
    path('review/', include('review.urls')),
]