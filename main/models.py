from django.conf import settings
from django.db import models
from accounts.models import CustomUser

# Create your models here.
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

RELATION_TYPE = [
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('spouse', 'Spouse'),
    ('child', 'Child'),
    ('sibling', 'Sibling'),
]

class Family(models.Model):
    """Each user has one family tree."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}'s Family"

class FamilyMember(models.Model):
    """Each person in the tree."""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Relationship(models.Model):
    """Defines how two members are related."""
    from_member = models.ForeignKey(FamilyMember, related_name='relationships_from', on_delete=models.CASCADE)
    to_member = models.ForeignKey(FamilyMember, related_name='relationships_to', on_delete=models.CASCADE)
    relation_type = models.CharField(max_length=10, choices=RELATION_TYPE)

    def __str__(self):
        return f"{self.from_member.name} is {self.relation_type} of {self.to_member.name}"