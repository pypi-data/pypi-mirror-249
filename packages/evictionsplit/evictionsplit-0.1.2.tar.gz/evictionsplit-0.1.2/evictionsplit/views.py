from typing import Optional

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Clocking, Eviction


def add_common_context(request, context: Optional[dict] = None) -> dict:
    """adds the common context used by all view"""
    context = context or {}
    new_context = {
        **{
            "user_has_manager_permission": request.user.has_perm(
                "evictionsplit.manager"
            ),
        },
        **context,
    }
    return new_context


@login_required
@permission_required("evictionsplit.basic_access")
def index(request):
    inactive_error = True if (request.GET.get("error") == "inactive") else False
    user = request.user
    user_active_evictions = user.evictions_participating.filter(active=True)
    for eviction in user_active_evictions:
        eviction.is_standby = eviction.is_user_on_standby(user)
        eviction.is_doorstop = eviction.is_user_on_doorstop(user)
        eviction.time_standby = eviction.user_standby_time(user)
        eviction.time_doorstop = eviction.user_doorstop_time(user)

    return render(
        request,
        "evictionsplit/index.html",
        add_common_context(
            request,
            {
                "inactive_error": inactive_error,
                "user_active_evictions": user_active_evictions,
            },
        ),
    )


@login_required
@permission_required("evictionsplit.basic_access")
def list_evictions(request):
    """Lists all active evictions that can be applied to join"""

    active_evictions = Eviction.objects.filter(active=True)
    user_active_evictions = request.user.evictions_participating.filter(active=True)

    return render(
        request,
        "evictionsplit/list.html",
        add_common_context(
            request,
            {
                "active_evictions": active_evictions,
                "user_active_evictions": user_active_evictions,
            },
        ),
    )


@login_required
@permission_required("evictionsplit.manager")
@require_POST
def new_eviction(request):
    eviction_name = request.POST.get("name")
    eviction = Eviction.create(eviction_name, request.user)
    eviction.save()

    return redirect("evictionsplit:list")


@login_required
@permission_required("evictionsplit.basic_access")
def apply(request, id):
    eviction = get_object_or_404(Eviction, id=id)
    eviction.user_apply(request.user)

    # TODO  make this work in models
    if request.user.has_perm("evictionsplit.manager"):
        eviction.validate_apply(request.user)

    return redirect("evictionsplit:list")


@login_required
@permission_required("evictionsplit.manager")
def accept_application(request, eviction_id, user_id):
    eviction = get_object_or_404(Eviction, id=eviction_id)
    user = get_object_or_404(User, id=user_id)
    eviction.validate_apply(user)

    return redirect("evictionsplit:eviction", eviction_id)


@login_required
@permission_required("evictionsplit.basic_access")
def eviction(request, id):
    eviction = get_object_or_404(Eviction, id=id)
    if not (eviction.active or request.user.has_perm("evictionsplit.manage")):
        return redirect("evictionsplit:index")
    is_standby = eviction.is_user_on_standby(request.user)
    is_doorstop = eviction.is_user_on_doorstop(request.user)
    unknown_change = request.GET.get("unknown")

    participants = []
    for participant in eviction.participants.all():
        participants.append(
            {
                "name": participant.profile.main_character.character_name,
                "portrait_url": participant.profile.main_character.portrait_url,
                "is_standby": eviction.is_user_on_standby(participant),
                "is_doorstop": eviction.is_user_on_doorstop(participant),
            }
        )

    applicants = []
    if eviction.has_applicants() and request.user.has_perm("evictionsplit.manager"):
        for applicant in eviction.get_applicants():
            applicants.append(
                {
                    "name": applicant.profile.main_character.character_name,
                    "id": applicant.id,
                    "portrait_url": applicant.profile.main_character.portrait_url,
                }
            )

    return render(
        request,
        "evictionsplit/eviction.html",
        add_common_context(
            request,
            {
                "eviction": eviction,
                "is_standby": is_standby,
                "is_doorstop": is_doorstop,
                "time_standby": eviction.user_standby_time(request.user),
                "time_doorstop": eviction.user_doorstop_time(request.user),
                "participants": participants,
                "applicants": applicants,
                "unknown_change": unknown_change,
            },
        ),
    )


@login_required
@permission_required("evictionsplit.basic_access")
@require_POST
def change_clocking(request, eviction_id):
    eviction = Eviction.objects.get(id=eviction_id)
    user = request.user
    if change := request.POST.get("change"):
        if change == "start":
            start = True
        elif change == "stop":
            start = False
        else:
            return redirect("evictionsplit:index")
    if request.POST.get("clocking_type") == Clocking.DOORSTOP:
        if start:
            eviction.user_start_doorstop(user)
        else:
            eviction.user_stop_doorstop(user)
    elif request.POST.get("clocking_type") == Clocking.STANDBY_FOR_PINGS:
        if start:
            eviction.user_start_standby_for_ping(user)
        else:
            eviction.user_stop_standby_for_ping(user)
    else:
        return redirect("evictionsplit:index")

    if request.POST.get("origin") == "eviction":
        return redirect("evictionsplit:eviction", eviction_id)
    else:
        return redirect("evictionsplit:index")


@login_required
@permission_required("evictionsplit.manager")
def management(request):
    active_evictions = Eviction.objects.filter(active=True)
    inactive_evictions = Eviction.objects.filter(active=False)

    return render(
        request,
        "evictionsplit/management.html",
        add_common_context(
            request,
            {
                "active_evictions": active_evictions,
                "inactive_evictions": inactive_evictions,
            },
        ),
    )


@login_required
@permission_required("evictionsplit.manager")
def stop_eviction(request, eviction_id):
    eviction = Eviction.objects.get(id=eviction_id)
    eviction.stop()

    return redirect("evictionsplit:manage")
