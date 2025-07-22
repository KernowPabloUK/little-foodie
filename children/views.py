from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Child
from .forms import AddChildForm


@login_required
def add_child(request):
    """
    Handle the addition of a new child to the user's profile.

    If the request is POST, validate and save the new child using AddChildForm.
    On success, redirect to the profile page with a success message.
    On GET, display an empty AddChildForm.
    Ensures the user has a profile; creates one if missing.
    """
    user = request.user

    try:
        profile = user.profile
    except AttributeError:
        from profiles.models import Profile
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        add_child_form = AddChildForm(request.POST)

        if add_child_form.is_valid():
            child = add_child_form.save(commit=False)
            child.user = profile
            child.save()
            messages.success(
                request, f'Child {child.name} added successfully!')
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


@login_required
def confirm_delete_child(request, child_id):
    """
    Display a confirmation page and handle deletion of a child.

    If the request is POST, delete the specified child
    belonging to the user's profile and redirect
    to the profile page with a success message.
    On GET, render a confirmation template.
    """
    child = get_object_or_404(Child, id=child_id, user=request.user.profile)

    if request.method == 'POST':
        child_name = child.name
        child.delete()
        messages.success(
            request,
            f'Child {child_name} has been deleted successfully.'
            )
        return redirect('profile')

    return render(
        request,
        'children/confirm_delete_child.html',
        {'child': child}
        )
