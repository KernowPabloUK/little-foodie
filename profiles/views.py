from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


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


# @login_required
# def update_child(request, child_id):
#     if request.method == 'POST':
#         child = get_object_or_404(Child, id=child_id, parent=request.user.profile)
#         form = ChildForm(request.POST, instance=child, parent=request.user.profile)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Child updated successfully!')
#         else:
#             messages.error(request, 'Please correct the errors below.')

#         return redirect('profile')

#     return redirect('profile')


# @login_required
# def add_child(request):
#     if request.method == 'POST':
#         form = AddChildForm(request.POST, parent=request.user.profile)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Child added successfully!')
#         else:
#             messages.error(request, 'Please correct the errors below.')

#         return redirect('profile')

#     return redirect('profile')
