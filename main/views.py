from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .models import FamilyMember
from django.shortcuts import get_object_or_404, render
from .utils import get_extended_family


# List all family members of the logged-in user
class FamilyTreeView(View):
    def get(self, request, pk):
        try:
            member = get_object_or_404(FamilyMember, pk=pk, family__user=request.user)
            tree = get_extended_family(member)
            return render(request, 'tree/family_tree.html', {'tree': tree, 'member': member})
        except:
            return render(request, 'tree/family_tree.html', {'tree': None, 'member': None})


class FamilyMemberCreateView(LoginRequiredMixin, CreateView):
    model = FamilyMember
    fields = ['name', 'gender', 'birth_date', 'death_date']
    template_name = 'tree/family_member_form.html'
    success_url = reverse_lazy('familyTree:family_tree')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
