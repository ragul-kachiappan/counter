from django.urls import path
from . import views

app_name = 'cubes'

urlpatterns = [
    # Cube URLs
    path('', views.home, name='home'),
    path('cube/create/', views.cube_create, name='cube_create'),
    path('cube/<int:cube_id>/', views.cube_detail, name='cube_detail'),
    path('cube/<int:cube_id>/update/', views.cube_update, name='cube_update'),
    path('cube/<int:cube_id>/delete/', views.cube_delete, name='cube_delete'),
    path('cube/<int:cube_id>/adjust-trees/', views.cube_adjust_trees, name='cube_adjust_trees'),
    
    # Tree URLs
    path('cube/<int:cube_id>/trees/', views.tree_list, name='tree_list'),
    path('cube/<int:cube_id>/tree/create/', views.tree_create, name='tree_create'),
    path('tree/<int:tree_id>/', views.tree_detail, name='tree_detail'),
    path('tree/<int:tree_id>/update/', views.tree_update, name='tree_update'),
    path('tree/<int:tree_id>/delete/', views.tree_delete, name='tree_delete'),
    path('cube/<int:cube_id>/trees/bulk-update/', views.tree_bulk_update, name='tree_bulk_update'),
    
    # AJAX URLs
    path('tree/<int:tree_id>/update-status/', views.tree_update_status_ajax, name='tree_update_status_ajax'),
]
