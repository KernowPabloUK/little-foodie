from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from children.forms import AddChildForm


# Create your views here.
def home_view(request):
    """
    Home page view - accessible to all users
    """
    return render(request, 'profiles/home.html')


@login_required
def profile_view(request):
    """
    Loads the profile page - logged in users only
    """
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'profile_form': profile_form,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def add_child(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        add_child_form = AddChildForm(request.POST)

        if add_child_form.is_valid():
            child = add_child_form.save(commit=False)
            child.user = profile
            child.save()
            messages.success(request, f'Child {child.name} added successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        add_child_form = AddChildForm()

    context = {
        'user': user,
        'profile': profile,
        'add_child_form': add_child_form,
    }

    return render(request, 'children/add_child.html', context)
