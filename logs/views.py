from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from children.models import Child
from .models import (
    FoodLog,
    Consistency,
    Preparation,
    FeedingMethod,
    SatisfactionLevel,
    Food,
)
from .forms import ChildSelectionForm, FoodLogForm, CreateFoodForm


@login_required
def food_log_view(request):
    """
    Display food logs for the selected child and handle new food log creation.

    If the user has more than one child, prompts for child selection.
    Handles form submission for logging new food entries and displays
    all logs for the selected child.
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

    create_food_form = CreateFoodForm()
    context = {
        'selected_child': selected_child,
        'children': children,
        'food_log_form': food_log_form,
        'create_food_form': create_food_form,
        'food_logs': food_logs,
        'show_child_selection': False
    }

    return render(request, 'logs/food_log.html', context)


@login_required
def clear_child_selection(request):
    """
    Clear the selected child from the session.

    Removes 'selected_child_id' from the session and
    redirects to the logs page.
    """
    if 'selected_child_id' in request.session:
        del request.session['selected_child_id']
    return redirect('logs')


@login_required
def edit_food_log(request, log_id):
    """
    Edit an existing food log entry.

    Loads the food log for editing, handles form submission, and updates
    the log with new data if the form is valid.
    """
    log = get_object_or_404(FoodLog, id=log_id, user=request.user)

    if request.method == 'POST':
        form = FoodLogForm(request.POST, instance=log)
        if form.is_valid():
            food_log = form.save(commit=False)
            log_datetime = form.cleaned_data.get('log_datetime')
            consistency_value = form.cleaned_data.get('consistency')
            preparation_value = form.cleaned_data.get('preparation')
            feeding_method_value = form.cleaned_data.get('feeding_method')
            satisfaction_value = form.cleaned_data.get('satisfaction_level')

            if consistency_value:
                consistency_obj, _ = Consistency.objects.get_or_create(
                    label=consistency_value
                )
                food_log.consistency = consistency_obj

            if preparation_value:
                preparation_obj, _ = Preparation.objects.get_or_create(
                    label=preparation_value
                )
                food_log.preparation = preparation_obj

            if feeding_method_value:
                feeding_method_obj, _ = FeedingMethod.objects.get_or_create(
                    label=feeding_method_value
                )
                food_log.feeding_method = feeding_method_obj

            if satisfaction_value:
                satisfaction_obj, _ = SatisfactionLevel.objects.get_or_create(
                    label=satisfaction_value
                )
                food_log.satisfaction_level = satisfaction_obj

            food_log.save()

            if log_datetime:
                FoodLog.objects.filter(id=food_log.id).update(
                    logged_at=log_datetime
                )

            messages.success(request, 'Food log updated successfully!')
            return redirect('logs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {
            'food': log.food,
            'log_datetime': log.logged_at,
            'preparation': log.preparation.label if log.preparation else '',
            'consistency': log.consistency.label if log.consistency else '',
            'feeding_method': (
                log.feeding_method.label if log.feeding_method else ''
            ),
            'volume': log.volume,
            'satisfaction_level': (
                log.satisfaction_level.label if log.satisfaction_level else ''
            ),
            'favourite': log.favourite,
            'notes': log.notes,
        }
        form = FoodLogForm(instance=log, initial=initial_data)

    return render(request, 'logs/edit_food_log.html', {
        'form': form,
        'log': log
    })


@login_required
@require_http_methods(["POST"])
def create_food_ajax(request):
    """
    Handle AJAX request to create a new food item.

    Validates input, checks for duplicates, creates the food if valid,
    and returns a JSON response with the result or error message.
    """
    try:
        name = request.POST.get('name', '').strip()
        name = name.title()
        category = request.POST.get('category', '').strip()
        min_age = request.POST.get('min_age_months')
        is_allergen = request.POST.get('is_allergen') == 'on'
        if not name or not category or not min_age:
            return JsonResponse({
                'success': False,
                'error': 'All required fields must be filled'
            })

        if Food.objects.filter(name__iexact=name).exists():
            return JsonResponse({
                'success': False,
                'error': (
                    f'A food with the name "{name}" already exists. '
                    'Please choose a different name.'
                )
            })

        food = Food.objects.create(
            name=name,
            category=int(category),
            min_age_months=int(min_age),
            is_allergen=is_allergen,
            created_by_user=request.user,
            is_authorised=False
        )

        return JsonResponse({
            'success': True,
            'food': {
                'id': food.id,
                'name': food.name,
                'category': food.get_category_display(),
                'min_age_months': food.min_age_months,
                'is_allergen': food.is_allergen,
                'is_authorised': food.is_authorised,
            }
        })

    except Exception as e:
        if ('duplicate key value' in str(e).lower() or
                'unique constraint' in str(e).lower()):
            return JsonResponse({
                'success': False,
                'error': (
                    f'A food with the name "{name}" already exists. '
                    'Please choose a different name.'
                )
            })
        return JsonResponse({
            'success': False,
            'error': (
                'An unexpected error occurred. Please try again.'
            )
        })


@login_required
def delete_food_log(request, log_id):
    """
    Delete a food log entry.

    Handles POST requests to delete the specified food log and
    redirects to the logs page.
    On GET, renders a confirmation page.
    """
    log = get_object_or_404(FoodLog, id=log_id, user=request.user)
    if request.method == "POST":
        log.delete()
        return redirect('logs')
    return render(request, 'logs/delete_food_log.html', {'log': log})
