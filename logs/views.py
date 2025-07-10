from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from children.models import Child
from .models import FoodLog
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
    
    # If no children, redirect to add child
    if not children.exists():
        messages.info(request, 'Please add a child before logging food.')
        return redirect('add_child')
    
    # Check if child is specified in URL or session
    selected_child_id = request.GET.get('child_id') or request.session.get('selected_child_id')
    selected_child = None
    
    if selected_child_id:
        try:
            selected_child = children.get(id=selected_child_id)
            request.session['selected_child_id'] = selected_child_id
        except Child.DoesNotExist:
            pass
    
    # If multiple children and none selected, show selection form
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
    
    # If only one child, use it
    if not selected_child and children.count() == 1:
        selected_child = children.first()
        request.session['selected_child_id'] = str(selected_child.id)
    
    # Handle food log form
    food_log_form = None
    if request.method == 'POST' and 'log_food' in request.POST:
        food_log_form = FoodLogForm(request.POST)
        if food_log_form.is_valid():
            food_log = food_log_form.save(commit=False)
            food_log.user = user
            food_log.child = selected_child
            
            # Handle the custom datetime field
            log_datetime = food_log_form.cleaned_data.get('log_datetime')
            if log_datetime:
                # Since logged_at has auto_now=True, we need to save first then update
                food_log.save()
                # Update the logged_at field manually
                FoodLog.objects.filter(id=food_log.id).update(logged_at=log_datetime)
            else:
                food_log.save()
                
            messages.success(request, f'Food logged successfully for {selected_child.name}!')
            return redirect('logs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        food_log_form = FoodLogForm()
    
    # Get existing food logs for the selected child
    food_logs = FoodLog.objects.filter(child=selected_child) if selected_child else []
    
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
