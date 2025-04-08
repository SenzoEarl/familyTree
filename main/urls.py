from django.urls import path
from .views import *

app_name = 'familyTree'

urlpatterns = [
    path('create/', FamilyMemberCreateView.as_view(), name='family_member_create'),
    path('<int:pk>/', FamilyTreeView.as_view(), name='tree'),

]
