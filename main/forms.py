from django import forms
from .models import Person, PersonRelationship, FamilyTree


class FamilyTreeForm(forms.ModelForm):
    class Meta:
        model = FamilyTree
        fields = ['name']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birth_date', 'gender']


class PersonRelationshipForm(forms.ModelForm):
    class Meta:
        model = PersonRelationship
        fields = ['from_person', 'to_person', 'relationship_type']

    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree', None)
        super().__init__(*args, **kwargs)
        if tree:
            self.fields['from_person'].queryset = tree.members.all()
            self.fields['to_person'].queryset = tree.members.all()
