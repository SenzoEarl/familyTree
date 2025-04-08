from django.urls import path
from .views import *

app_name = 'familyTree'

urlpatterns = [
    path('', MyTreesView.as_view(), name='my_trees'),
    path('create/', FamilyTreeCreateView.as_view(), name='create_tree'),
    path('<int:tree_id>/add-person/', PersonCreateView.as_view(), name='add_person'),
    path('<int:tree_id>/add-relationship/', PersonRelationshipCreateView.as_view(), name='add_relationship'),
    path('<int:pk>/', FamilyTreeDetailView.as_view(), name='view_tree'),

]
