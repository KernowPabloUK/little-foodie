from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from children.models import Child
from .models import (
    FoodLog,
    Consistency,
    Preparation,
    FeedingMethod,
    SatisfactionLevel,
)
from .forms import ChildSelectionForm, FoodLogForm


@login_required
def food_log_view(request):
    """
    Display food logs and handle new food log creation
    """
    user = request.user

    try:
        profile = user.profile
    except AttributeError:
        from profiles.models import Profile
        profile = Profile.objects.create(user=user)

    children = profile.children.all()

    if not children.exists():
        messages.info(request, 'Please add a child before logging food.')
        return redirect('add_child')

    selected_child_id = (
        request.GET.get('child_id') or
        request.session.get('selected_child_id')
    )
    selected_child = None

    if selected_child_id:
        try:
            selected_child = children.get(id=selected_child_id)
            request.session['selected_child_id'] = selected_child_id
        except Child.DoesNotExist:
            pass

    if children.count() > 1 and not selected_child:
        if request.method == 'POST':
            child_form = ChildSelectionForm(user=user, data=request.POST)
            if child_form.is_valid():
                selected_child = child_form.cleaned_data['child']
                request.session['selected_child_id'] = str(selected_child.id)
                return redirect('logs')
        else:
            child_form = ChildSelectionForm(user=user)

        context = {
            'child_form': child_form,
            'children': children,
            'show_child_selection': True
        }
        return render(request, 'logs/food_log.html', context)

    if not selected_child and children.count() == 1:
        selected_child = children.first()
        request.session['selected_child_id'] = str(selected_child.id)

    food_log_form = None
    if request.method == 'POST' and 'log_food' in request.POST:
        food_log_form = FoodLogForm(request.POST)
        if food_log_form.is_valid():
            food_log = food_log_form.save(commit=False)
            food_log.user = user
            food_log.child = selected_child

            log_datetime = food_log_form.cleaned_data.get('log_datetime')

            consistency_value = food_log_form.cleaned_data.get('consistency')
            preparation_value = food_log_form.cleaned_data.get('preparation')
            feeding_method_value = food_log_form.cleaned_data.get(
                'feeding_method'
            )
            satisfaction_value = food_log_form.cleaned_data.get(
                'satisfaction_level'
            )

            consistency_obj, _ = Consistency.objects.get_or_create(
                label=consistency_value
            )
            preparation_obj, _ = Preparation.objects.get_or_create(
                label=preparation_value
            )
            feeding_method_obj, _ = FeedingMethod.objects.get_or_create(
                label=feeding_method_value
            )
            satisfaction_obj, _ = SatisfactionLevel.objects.get_or_create(
                label=satisfaction_value
            )

            food_log.consistency = consistency_obj
            food_log.preparation = preparation_obj
            food_log.feeding_method = feeding_method_obj
            food_log.satisfaction_level = satisfaction_obj

            food_log.save()

            if log_datetime:
                FoodLog.objects.filter(id=food_log.id).update(
                    logged_at=log_datetime
                )

            messages.success(
                request,
                f'Food logged successfully for {selected_child.name}!'
            )
            return redirect('logs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        food_log_form = FoodLogForm()

    food_logs = (
        FoodLog.objects.filter(child=selected_child).order_by('-logged_at')
        if selected_child else []
    )

    context = {
        'selected_child': selected_child,
        'children': children,
        'food_log_form': food_log_form,
        'food_logs': food_logs,
        'show_child_selection': False
    }

    return render(request, 'logs/food_log.html', context)


@login_required
def clear_child_selection(request):
    """Clear the selected child from session"""
    if 'selected_child_id' in request.session:
        del request.session['selected_child_id']
    return redirect('logs')
