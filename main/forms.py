from django import forms
from .models import FamilyMember

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'gender', 'birth_date', 'death_date', 'father', 'mother']

    def clean(self):
        cleaned_data = super().clean()
        father = cleaned_data.get('father')
        mother = cleaned_data.get('mother')

        # Ensure at least one parent is provided
        if not father and not mother:
            raise forms.ValidationError('A family member must have at least one parent.')

        return cleaned_data