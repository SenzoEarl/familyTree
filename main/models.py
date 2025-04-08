from django.conf import settings
from django.db import models
from accounts.models import CustomUser


# Create your models here.
class FamilyTree(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trees')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Person(models.Model):
    family_tree = models.ForeignKey(FamilyTree, on_delete=models.CASCADE, related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                              null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.family_tree.name})"


class RelationshipType(models.Model):
    """Defines the type of relationship (e.g., parent, spouse, sibling)."""
    name = models.CharField(max_length=50)  # e.g., parent, spouse, sibling, etc.
    bidirectional = models.BooleanField(default=False)  # e.g., sibling/spouse are bidirectional, parent/child are not

    def __str__(self):
        return self.name


class PersonRelationship(models.Model):
    """Represents a directional relationship between two people."""
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='from_relationships')
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='to_relationships')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    family_tree = models.ForeignKey(FamilyTree, on_delete=models.CASCADE, related_name='relationships')

    class Meta:
        unique_together = ('from_person', 'to_person', 'relationship_type')

    def __str__(self):
        return f"{self.from_person} → {self.relationship_type.name} → {self.to_person}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.from_person.family_tree != self.to_person.family_tree:
            raise ValidationError("Both people must belong to the same family tree.")

        if self.from_person == self.to_person:
            raise ValidationError("A person cannot be in a relationship with themselves.")
