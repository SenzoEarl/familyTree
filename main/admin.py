from django.contrib import admin

from main.models import FamilyTree, Person, RelationshipType, PersonRelationship

# Register your models here.
admin.site.register(FamilyTree)
admin.site.register(Person)
admin.site.register(RelationshipType)
admin.site.register(PersonRelationship)