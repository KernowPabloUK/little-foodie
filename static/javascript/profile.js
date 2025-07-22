document.addEventListener('DOMContentLoaded', function () {
    /**
     * Auto-dismisses alert messages after 3 seconds.
     */
    const alerts = document.querySelectorAll('.messages .alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.style.display = 'none';
            }
        }, 3000);
    });
});
