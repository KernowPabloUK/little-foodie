from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


def home_view(request):
    """
    Render the home page.

    This view is accessible to all users, authenticated or not.
    Returns the rendered 'profiles/home.html' template.
    """
    return render(request, 'profiles/home.html')


@login_required
def profile_view(request):
    """
    Display and handle updates to the user's profile page.

    Loads the profile page for logged-in users only. Handles GET requests to
    display the profile and POST requests to update the profile information.
    If the user does not have a profile, one is created. Displays success or
    error messages based on form validation.
    """
    user = request.user
    edit_mode = request.GET.get('edit', False)

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
            edit_mode = True
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'profile_form': profile_form,
        'edit_mode': edit_mode,
    }

    return render(request, 'profiles/profile.html', context)
