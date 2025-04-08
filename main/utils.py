# familytree/utils.py

from .models import *


def get_extended_family(member):
    tree = {
        'self': member,
        'parents': [],
        'children': [],
        'siblings': [],
        'spouse': [],
        'grandparents': [],
        'aunts_uncles': [],
        'cousins': [],
    }

    def related(from_member, relation_type):
        return FamilyMember.objects.filter(
            pk__in=Relationship.objects.filter(from_member=from_member, relation_type=relation_type)
            .values_list('to_member', flat=True)
        )

    tree['parents'] = list(related(member, 'father')) + list(related(member, 'mother'))
    tree['children'] = list(related(member, 'child'))
    tree['spouse'] = list(related(member, 'spouse'))

    # Siblings
    siblings = set()
    for p in tree['parents']:
        children = related(p, 'child')
        for child in children:
            if child != member:
                siblings.add(child)
    tree['siblings'] = list(siblings)

    # Grandparents
    grandparents = set()
    for p in tree['parents']:
        grandparents |= set(related(p, 'father')) | set(related(p, 'mother'))
    tree['grandparents'] = list(grandparents)

    # Aunts and uncles
    aunts_uncles = set()
    for gp in tree['grandparents']:
        children = related(gp, 'child')
        for child in children:
            if child not in tree['parents']:
                aunts_uncles.add(child)
    tree['aunts_uncles'] = list(aunts_uncles)

    # Cousins
    cousins = set()
    for au in tree['aunts_uncles']:
        cousins |= set(related(au, 'child'))
    tree['cousins'] = list(cousins)

    return tree
