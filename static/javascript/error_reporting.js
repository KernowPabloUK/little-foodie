document.addEventListener('DOMContentLoaded', function() {
    var reasonSelect = document.getElementById('contactReason');
    var detailsGroup = document.getElementById('contactDetailsGroup');
    var foodErrorOptions = document.getElementById('foodErrorOptions');
    var contactForm = document.getElementById('contactForm');
    var contactFormFields = document.getElementById('contactFormFields');
    var contactThanks = document.getElementById('contactThanks');
    var contactModal = document.getElementById('contactModal');

    // Show/hide details and food error options based on reason selection
    reasonSelect.addEventListener('change', function() {
        if (this.value) {
            detailsGroup.style.display = 'block';
        } else {
            detailsGroup.style.display = 'none';
        }
        if (this.value === 'food') {
            foodErrorOptions.style.display = 'block';
        } else {
            foodErrorOptions.style.display = 'none';
        }
    });

    // Show thank you message on form submit
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        contactFormFields.style.display = 'none';
        contactThanks.style.display = 'block';
    });

    // Reset form and UI state when modal is closed
    contactModal.addEventListener('hidden.bs.modal', function () {
        contactForm.reset();
        contactFormFields.style.display = 'block';
        contactThanks.style.display = 'none';
        foodErrorOptions.style.display = 'none';
        detailsGroup.style.display = 'none';
    });
});