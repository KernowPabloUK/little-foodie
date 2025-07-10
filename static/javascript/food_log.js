document.addEventListener('DOMContentLoaded', function() {
    const foodSelect = document.getElementById('food-select');
    if (foodSelect) {
        foodSelect.addEventListener('change', handleFoodSelection);
    }

    const satisfactionOptions = document.querySelectorAll('.satisfaction-option');
    satisfactionOptions.forEach(option => {
        option.addEventListener('click', function() {
            satisfactionOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            const value = this.getAttribute('data-value');
            document.getElementById('satisfaction_level').value = value;
        });
    });

    const favouriteToggle = document.querySelector('.favourite-toggle');
    if (favouriteToggle) {
        favouriteToggle.addEventListener('click', function() {
            const isSelected = this.getAttribute('data-selected') === 'true';
            const newState = !isSelected;
            this.setAttribute('data-selected', newState);
            document.getElementById('favourite').value = newState.toString();
        });
    }
});

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

function handleFoodSelection() {
    const foodSelect = document.getElementById('food-select');
    const selectedOption = foodSelect.options[foodSelect.selectedIndex];
    
    console.log('Food selected:', selectedOption.value, selectedOption.text);
    
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
                console.log('Food data received:', data);
                document.getElementById('food-category').value = data.category || 'Unknown';
                
                const minAgeElement = document.getElementById('min-age');
                if (minAgeElement) {
                    minAgeElement.textContent = data.min_age_months || 'Not specified';
                }
                
                const foodImageContainer = document.getElementById('food-image-container');
                const foodImage = document.getElementById('food-image');
                
                if (data.image && foodImage) {
                    foodImage.src = data.image;
                    foodImage.onerror = function() {
                        console.log('Image failed to load:', data.image);
                        foodImageContainer.style.display = 'none';
                    };
                    foodImage.onload = function() {
                        console.log('Image loaded successfully:', data.image);
                        foodImageContainer.style.display = 'block';
                    };
                    foodImageContainer.style.display = 'block';
                } else {
                    console.log('No image URL provided');
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
                
                showFormSections();
            })
            .catch(error => {
                console.error('Error fetching food details:', error);
                document.getElementById('food-category').value = 'Error loading category';
                
                hideFormSections();
            });
    } else {
        document.getElementById('food-category').value = '';
        
        hideFormSections();
    }
}

function clearForm() {
    if (confirm('Are you sure you want to clear the form?')) {
        document.getElementById('food-log-form').reset();
        document.getElementById('food-category').value = '';
        
        hideFormSections();
        
        document.querySelectorAll('.satisfaction-option').forEach(opt => opt.classList.remove('selected'));
        document.getElementById('satisfaction_level').value = '';
        
        const favouriteToggle = document.querySelector('.favourite-toggle');
        if (favouriteToggle) {
            favouriteToggle.setAttribute('data-selected', 'false');
            document.getElementById('favourite').value = 'false';
        }
    }
}