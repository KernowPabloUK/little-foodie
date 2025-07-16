document.addEventListener('DOMContentLoaded', function() {
    if (typeof foodData === 'undefined') return;
    const ctx = document.getElementById('foodStatsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: foodData.labels.map(l => l.name ? l.name : l), // support both formats
            datasets: [{
                label: 'Times Eaten',
                data: foodData.counts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    }
                }
            }
        }
    });

    document.querySelectorAll('input[name="child"]').forEach(radio => {
        radio.addEventListener('change', function() {
            window.location.href = '?child_id=' + this.value;
        });
    });
});