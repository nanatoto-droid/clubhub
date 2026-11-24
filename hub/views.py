from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .forms import JoinForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Club, Event, JoinRequest


@login_required
@require_POST
def approve_request(request, pk):
    if not request.user.is_staff_member():
        messages.error(request, 'Only staff can approve requests.')
        return redirect('accounts:dashboard')
    jr = get_object_or_404(JoinRequest, pk=pk)
    jr.status = 'approved'
    jr.save()
    messages.success(request, f'Approved {jr.name} for {jr.club.name}.')
    return redirect('accounts:dashboard')


@login_required
@require_POST
def reject_request(request, pk):
    if not request.user.is_staff_member():
        messages.error(request, 'Only staff can reject requests.')
        return redirect('accounts:dashboard')
    jr = get_object_or_404(JoinRequest, pk=pk)
    jr.status = 'rejected'
    jr.save()
    messages.success(request, f'Rejected {jr.name}\'s request.')
    return redirect('accounts:dashboard')


def home(request):
    clubs = Club.objects.annotate(member_count=Count('join_requests'))
    featured = clubs.order_by('-member_count')[:3]
    categories = Club._meta.get_field('category').choices
    upcoming = Event.objects.select_related('club').order_by('date')[:3]
    return render(request, 'hub/home.html', {
        'clubs': clubs,
        'featured': featured,
        'categories': categories,
        'upcoming': upcoming,
    })


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    events = club.events.all()
    member_count = club.join_requests.count()
    return render(request, 'hub/club_detail.html', {
        'club': club,
        'events': events,
        'member_count': member_count,
    })


def events(request):
    all_events = Event.objects.select_related('club').all()
    return render(request, 'hub/events.html', {'events': all_events})


def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            jr = form.save(commit=False)
            if request.user.is_authenticated:
                jr.user = request.user
            jr.save()
            messages.success(request, 'Thanks! Your join request has been recorded.')
            return redirect('hub:join')
    else:
        form = JoinForm()
    return render(request, 'hub/join.html', {'form': form})