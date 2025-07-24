document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismisses alert messages after 3 seconds.
    const alerts = document.querySelectorAll(".alert:not(.food-warning)");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });

    // Attach change event to food select to fetch and display food details.
    const foodSelect = document.getElementById('food-select');
    if (foodSelect) {
        foodSelect.addEventListener('change', handleFoodSelection);
    }

    // Handle satisfaction level selection by updating UI and hidden input.
    const satisfactionOptions = document.querySelectorAll('.satisfaction-option');
    satisfactionOptions.forEach(option => {
        option.addEventListener('click', function() {
            satisfactionOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            const value = this.getAttribute('data-value');
            document.getElementById('satisfaction_level').value = value;
        });
    });

    // Handle favourite toggle button and update hidden input.
    const favouriteToggle = document.querySelector('.favourite-toggle');
    if (favouriteToggle) {
        favouriteToggle.addEventListener('click', function() {
            const isSelected = this.getAttribute('data-selected') === 'true';
            const newState = !isSelected;
            this.setAttribute('data-selected', newState);
            document.getElementById('favourite').value = newState.toString();
        });
    }

    // Attach clear form button to reset the form and UI.
    const clearFormBtn = document.getElementById('clear-form-btn');
    if (clearFormBtn) {
        clearFormBtn.addEventListener('click', clearForm);
    }

    // Handle new food creation via AJAX and update the food select.
    const saveFoodBtn = document.getElementById('saveFoodBtn');
    const newFoodForm = document.getElementById('newFoodForm');
    
    if (saveFoodBtn) {
        saveFoodBtn.addEventListener('click', function() {
            const formData = new FormData(newFoodForm);
            
            const name = formData.get('name');
            const category = formData.get('category');
            const minAge = formData.get('min_age_months');
            
            if (!name || name.trim() === '' || !category || category === '' || !minAge || minAge === '') {
                let missingFields = [];
                if (!name || name.trim() === '') missingFields.push('Food Name');
                if (!category || category === '') missingFields.push('Category');
                if (!minAge || minAge === '') missingFields.push('Minimum Age');
                
                alert('Please fill in all required fields: ' + missingFields.join(', '));
                return;
            }
            
            // Send AJAX request to create new food
            fetch('/logs/foods/create/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const foodSelect = document.getElementById('food-select');
                    const newOption = new Option(data.food.name, data.food.id, true, true);
                    foodSelect.add(newOption);
                    
                    foodSelect.value = data.food.id;
                    foodSelect.dispatchEvent(new Event('change'));                      
                    
                    const newFoodModal = bootstrap.Modal.getInstance(document.getElementById('newFoodModal'));
                    newFoodModal.hide();
                    newFoodForm.reset();
                    
                    showAlert('Food created successfully!', 'success');
                } else {
                    alert('Error creating food: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Error creating food. Please try again.');
            });
        });
    }
    
    // Show a Bootstrap alert message at the top of the container.
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 3000);
    }
});

// Show all relevant form sections when a food is selected.
function showFormSections() {
    const sectionsToShow = [
        'food-details',
        'preparation-section',
        'volume-section',
        'satisfaction-section',
        'favourite-section',
        'notes-section'
    ];
    
    sectionsToShow.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
        }
    });
}

// Hide all form sections, used when no food is selected or on form clear.
function hideFormSections() {
    const sectionsToHide = [
        'food-details',
        'food-image-container',
        'preparation-section',
        'volume-section',
        'satisfaction-section',
        'favourite-section',
        'notes-section'
    ];
    
    sectionsToHide.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'none';
        }
    });
}

// Handle food selection changes.
// Fetches food details from the API and updates the UI accordingly.
// Shows/hides warnings and updates image, category, and favourite state.
function handleFoodSelection() {
    const foodSelect = document.getElementById('food-select');
    const selectedOption = foodSelect.options[foodSelect.selectedIndex];
    
    if (selectedOption.value) {
        document.getElementById('food-category').value = 'Loading...';
        
        fetch(`/foods/api/details/${selectedOption.value}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('food-category').value = data.category || 'Unknown';
                
                const minAgeElement = document.getElementById('min-age');
                if (minAgeElement) {
                    minAgeElement.textContent = data.min_age_months || 'Not specified';
                }
                
                const ageWarning = document.getElementById('age-warning');
                const childAgeInput = document.getElementById('child-age-months');
                if (ageWarning && childAgeInput && data.min_age_months) {
                    const childAgeMonths = parseInt(childAgeInput.value, 10);
                    if (childAgeMonths < data.min_age_months) {
                        ageWarning.style.display = 'block';
                    } else {
                        ageWarning.style.display = 'none';
                    }
                } else if (ageWarning) {
                    ageWarning.style.display = 'none';
                }
                
                const foodImageContainer = document.getElementById('food-image-container');
                const foodImage = document.getElementById('food-image');
                
                if (foodImage) {
                    if (!data.image || data.is_authorised === false || data.is_authorised === "false") {
                        foodImage.src = "/static/images/food_images/non_authorised_food_warning.png";
                        foodImageContainer.style.display = 'block';
                    } else {
                        foodImage.src = data.image;
                        foodImage.onerror = function() {
                            foodImageContainer.style.display = 'none';
                        };
                        foodImage.onload = function() {
                            foodImageContainer.style.display = 'block';
                        };
                        foodImageContainer.style.display = 'block';
                    }
                } else {
                    foodImageContainer.style.display = 'none';
                }
                
                const allergenWarning = document.getElementById('allergen-warning');
                if (allergenWarning) {
                    if (data.is_allergen) {
                        allergenWarning.style.display = 'block';
                    } else {
                        allergenWarning.style.display = 'none';
                    }
                }
                
                const favouriteToggle = document.querySelector('.favourite-toggle');
                if (favouriteToggle && data.is_favourite !== undefined) {
                    const isFavourite = data.is_favourite;
                    favouriteToggle.setAttribute('data-selected', isFavourite.toString());
                    document.getElementById('favourite').value = isFavourite.toString();
                } else if (favouriteToggle) {
                    favouriteToggle.setAttribute('data-selected', 'false');
                    document.getElementById('favourite').value = 'false';
                }
                
                const authorisationWarning = document.getElementById('authorisation-warning');
                if (authorisationWarning) {
                    if (data.is_authorised === false || data.is_authorised === "false") {
                        authorisationWarning.style.display = 'block';
                    } else {
                        authorisationWarning.style.display = 'none';
                    }
                }
                
                showFormSections();
            })
            .catch(error => {
                document.getElementById('food-category').value = 'Error loading category';
                
                hideFormSections();
            });
    } else {
        document.getElementById('food-category').value = '';
        
        hideFormSections();
    }
}

// Clear the food log form and reset all UI elements to their default state.
function clearForm() {
    if (confirm('Are you sure you want to clear the form?')) {
        document.getElementById('food-log-form').reset();
        
        const foodSelect = document.getElementById('food-select');
        if (foodSelect) {
            foodSelect.selectedIndex = 0;
        }
        
        document.getElementById('food-category').value = '';
        
        const preparation = document.getElementById('id_preparation');
        if (preparation) preparation.selectedIndex = 0;
        
        const consistency = document.getElementById('id_consistency');
        if (consistency) consistency.selectedIndex = 0;
        
        const feedingMethod = document.getElementById('id_feeding_method');
        if (feedingMethod) feedingMethod.selectedIndex = 0;
        
        document.getElementById('id_volume').value = '';
        document.getElementById('satisfaction_level').value = '';
        document.getElementById('favourite').value = 'false';
        document.querySelectorAll('.satisfaction-option').forEach(opt => opt.classList.remove('selected'));
        
        const favouriteToggle = document.querySelector('.favourite-toggle');
        if (favouriteToggle) {
            favouriteToggle.setAttribute('data-selected', 'false');
        }
        
        hideFormSections();
    }
}