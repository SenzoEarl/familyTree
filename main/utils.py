from main.models import *


# familytree/utils.py

def get_extended_family(member):
    """Returns extended family as dict."""
    tree = {
        'self': member,
        'parents': [],
        'siblings': [],
        'children': [],
        'spouse': None,
        'grandparents': [],
        'aunts_uncles': [],
        'cousins': [],
    }

    # Parents
    parents = Relationship.objects.filter(from_member=member, relation_type__in=['father', 'mother']).values_list(
        'to_member', flat=True)
    tree['parents'] = FamilyMember.objects.filter(id__in=parents)

    # Children
    children = Relationship.objects.filter(from_member=member, relation_type='child').values_list('to_member',
                                                                                                  flat=True)
    tree['children'] = FamilyMember.objects.filter(id__in=children)

    # Spouse
    spouse_rel = Relationship.objects.filter(from_member=member, relation_type='spouse').first()
    tree['spouse'] = spouse_rel.to_member if spouse_rel else None

    # Siblings (shared parents)
    sibling_ids = set()
    for parent in tree['parents']:
        siblings = Relationship.objects.filter(from_member=parent, relation_type='child').exclude(to_member=member)
        for s in siblings:
            sibling_ids.add(s.to_member.id)
    tree['siblings'] = FamilyMember.objects.filter(id__in=sibling_ids)

    # Grandparents (parents of parents)
    grandparent_ids = set()
    for parent in tree['parents']:
        grand_rels = Relationship.objects.filter(from_member=parent, relation_type__in=['father', 'mother'])
        for rel in grand_rels:
            grandparent_ids.add(rel.to_member.id)
    tree['grandparents'] = FamilyMember.objects.filter(id__in=grandparent_ids)

    # Aunts/Uncles = siblings of parents
    aunt_uncle_ids = set()
    for parent in tree['parents']:
        parent_parents = Relationship.objects.filter(from_member=parent, relation_type__in=['father', 'mother'])
        for gp in parent_parents:
            siblings = Relationship.objects.filter(from_member=gp.to_member, relation_type='child').exclude(
                to_member=parent)
            for rel in siblings:
                aunt_uncle_ids.add(rel.to_member.id)
    tree['aunts_uncles'] = FamilyMember.objects.filter(id__in=aunt_uncle_ids)

    # Cousins = children of aunts/uncles
    cousin_ids = set()
    for au in tree['aunts_uncles']:
        cousin_rels = Relationship.objects.filter(from_member=au, relation_type='child')
        for rel in cousin_rels:
            cousin_ids.add(rel.to_member.id)
    tree['cousins'] = FamilyMember.objects.filter(id__in=cousin_ids)

    return tree
