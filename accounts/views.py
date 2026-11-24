from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from hub.models import JoinRequest, Event


def signup(request):
    if request.user.is_authenticated:
        return redirect('hub:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hub:home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_staff_member():
        requests = JoinRequest.objects.select_related('club', 'user').all()
        return render(request, 'accounts/dashboard.html', {
            'requests': requests,
            'is_staff_member': True,
        })

    # Student dashboard
    my_requests = (
        JoinRequest.objects
        .filter(user=request.user)
        .select_related('club')
        .order_by('-submitted_at')
    )
    approved = my_requests.filter(status='approved')
    approved_clubs = [r.club for r in approved]
    events = Event.objects.filter(club__in=approved_clubs).select_related('club').order_by('date') if approved_clubs else []
    return render(request, 'accounts/dashboard.html', {
        'is_staff_member': False,
        'my_requests': my_requests,
        'approved_clubs': approved_clubs,
        'events': events,
    })