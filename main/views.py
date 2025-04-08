import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from .forms import *
from .models import *
from .utils import get_extended_family


# List all family members of the logged-in user
class MyTreesView(LoginRequiredMixin, ListView):
    model = FamilyTree
    template_name = 'tree/family_tree.html'
    context_object_name = 'trees'

    def get_queryset(self):
        return FamilyTree.objects.filter(owner=self.request.user)


class FamilyTreeCreateView(LoginRequiredMixin, CreateView):
    model = FamilyTree
    form_class = FamilyTreeForm
    template_name = 'tree/create_family_tree.html'
    success_url = reverse_lazy('familyTree:my_trees')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'tree/add_person.html'

    def dispatch(self, request, *args, **kwargs):
        self.tree = get_object_or_404(FamilyTree, id=kwargs['tree_id'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.family_tree = self.tree
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('familyTree:view_tree', kwargs={'pk': self.tree.id})


class FamilyTreeDetailView(LoginRequiredMixin, DetailView):
    model = FamilyTree
    template_name = 'tree/view_family_tree.html'
    context_object_name = 'tree'

    def get_queryset(self):
        return FamilyTree.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tree = self.object

        people = {p.id: p for p in tree.members.all()}
        relationships = tree.relationships.all()

        # Categorize relationships
        parent_links = relationships.filter(relationship_type__name="parent")
        spouse_links = relationships.filter(relationship_type__name="spouse")

        children_map = {}
        spouses_map = {}

        for rel in parent_links:
            parent_id = rel.from_person.id
            child_id = rel.to_person.id
            children_map.setdefault(parent_id, []).append(child_id)

        for rel in spouse_links:
            a, b = rel.from_person.id, rel.to_person.id
            spouses_map.setdefault(a, set()).add(b)
            spouses_map.setdefault(b, set()).add(a)

        # Keep track of added nodes to avoid duplicates
        added_nodes = {}

        def build_node(person_id, parent_ref=None):
            if person_id in added_nodes:
                return added_nodes[person_id]

            person = people[person_id]
            node = {
                "text": {
                    "name": f"{person.first_name} {person.last_name}",
                    "title": person.gender or ""
                },
                "HTMLclass": "nodeExample1",
            }

            added_nodes[person_id] = node

            # Handle spouse
            spouse_ids = spouses_map.get(person_id, [])
            if spouse_ids:
                spouse_id = list(spouse_ids)[0]
                if spouse_id not in added_nodes:
                    spouse = build_node(spouse_id)
                else:
                    spouse = added_nodes[spouse_id]

                marriage_node = {
                    "children": [],
                    "stackChildren": True,
                    "HTMLclass": "marriageNode",
                    "pseudo": True,
                    "connectors": {"type": "step"},
                    "marriage": [node, added_nodes[spouse_id]]
                }

                # Find their children
                children = set(children_map.get(person_id, [])) | set(children_map.get(spouse_id, []))
                marriage_node["children"] = [build_node(child_id) for child_id in children]

                return marriage_node

            # If no spouse, handle their children directly
            if person_id in children_map:
                node["children"] = [build_node(child_id) for child_id in children_map[person_id]]

            return node

        # Find root(s)
        all_children = {rel.to_person.id for rel in parent_links}
        roots = [p.id for p in people.values() if p.id not in all_children]

        tree_data = {
            "text": {"name": "Family Tree", "title": tree.name},
            "children": [build_node(root_id) for root_id in roots]
        }

        context['tree_data'] = mark_safe(json.dumps(tree_data))
        return context


class PersonRelationshipCreateView(LoginRequiredMixin, CreateView):
    model = PersonRelationship
    form_class = PersonRelationshipForm
    template_name = 'tree/add_relationship.html'

    def dispatch(self, request, *args, **kwargs):
        self.tree = get_object_or_404(FamilyTree, pk=kwargs['tree_id'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tree'] = self.tree
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        form.instance.family_tree = self.tree
        response = super().form_valid(form)

        # Automatically create reverse relationship if applicable
        if form.instance.relationship_type.bidirectional:
            PersonRelationship.objects.get_or_create(
                from_person=form.instance.to_person,
                to_person=form.instance.from_person,
                relationship_type=form.instance.relationship_type,
                family_tree=self.tree
            )
        return response

    def get_success_url(self):
        return reverse_lazy('familyTree:view_tree', kwargs={'pk': self.tree.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tree'] = self.tree
        return context
