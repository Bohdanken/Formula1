from django import template
from formula.models import TeamMember

register = template.Library()

@register.filter
def is_team_member(user):
    return TeamMember.objects.filter(user=user).exists()

@register.filter
def team(user):
    try:
        team_member = TeamMember.objects.get(user=user)
        return team_member.team
    except TeamMember.DoesNotExist:
        return None
