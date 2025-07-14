document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });

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