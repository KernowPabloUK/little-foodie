document.addEventListener('DOMContentLoaded', function() {
    // --- Times Eaten Horizontal Bar Chart ---
    if (typeof foodData === 'undefined') return;
    const ctx = document.getElementById('foodStatsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: foodData.labels.map(l => l.name ? l.name : l),
            datasets: [{
                label: 'Times Eaten',
                data: foodData.counts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    }
                }
            }
        }
    });

    // --- Volume Horizontal Bar Chart ---
    if (typeof foodData.volumes !== 'undefined') {
        const ctxVolume = document.getElementById('foodVolumeChart').getContext('2d');
        new Chart(ctxVolume, {
            type: 'bar',
            data: {
                labels: foodData.labels.map(l => l.name ? l.name : l),
                datasets: [{
                    label: 'Total Volume (teaspoons)',
                    data: foodData.volumes,
                    backgroundColor: 'rgba(255, 159, 64, 0.6)'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    document.querySelectorAll('input[name="child"]').forEach(radio => {
        radio.addEventListener('change', function() {
            window.location.href = '?child_id=' + this.value;
        });
    });
});