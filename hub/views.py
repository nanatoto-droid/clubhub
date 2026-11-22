from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Club, Event
from .forms import JoinForm


def home(request):
    clubs = Club.objects.all()
    return render(request, 'hub/home.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    events = club.events.all()
    return render(request, 'hub/club_detail.html', {'club': club, 'events': events})


def events(request):
    all_events = Event.objects.select_related('club').all()
    return render(request, 'hub/events.html', {'events': all_events})


def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! Your join request has been recorded.')
            return redirect('hub:join')
    else:
        form = JoinForm()
    return render(request, 'hub/join.html', {'form': form})