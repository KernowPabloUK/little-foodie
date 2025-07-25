document.addEventListener('DOMContentLoaded', function() {
    let chart1, chart2;

    // Render bar charts for food or category statistics.
    // Destroys previous charts before rendering new ones.
    function renderCharts(data) {
        if (chart1) chart1.destroy();
        if (chart2) chart2.destroy();

        const ctx = document.getElementById('foodStatsChart').getContext('2d');
        chart1 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels.map(l => l.name),
                datasets: [{
                    label: 'Times Eaten',
                    data: data.counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                scales: {
                    x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
                }
            }
        });

        const ctxVolume = document.getElementById('foodVolumeChart').getContext('2d');
        chart2 = new Chart(ctxVolume, {
            type: 'bar',
            data: {
                labels: data.labels.map(l => l.name),
                datasets: [{
                    label: '(teaspoons)',
                    data: data.volumes,
                    backgroundColor: 'rgba(255, 159, 64, 0.6)'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                scales: {
                    x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
                }
            }
        });
    }

    // Render the satisfaction table, showing foods by satisfaction level.
    function renderSatisfactionTable(data) {
        const table = document.querySelector('.satisfaction-table tbody tr');
        table.innerHTML = '';
        for (let s of [3, 2, 1, 0]) {
            let cell = document.createElement('td');
            let found = false;
            data.labels.forEach(label => {
                if (label.satisfaction === s) {
                    let div = document.createElement('div');
                    div.className = 'satisfaction-food';
                    if (label.image) {
                        let img = document.createElement('img');
                        img.src = '/static/' + label.image.replace(/^\/+/, '');
                        img.alt = label.name;
                        img.style.maxWidth = '60px';
                        img.style.maxHeight = '60px';
                        img.style.display = 'block';
                        img.style.margin = '0 auto';
                        div.appendChild(img);
                    } else {
                        div.textContent = label.name;
                        div.style.fontSize = '0.85em';
                    }
                    cell.appendChild(div);
                    found = true;
                }
            });
            if (!found) {
                let span = document.createElement('span');
                span.className = 'satisfaction-empty';
                span.textContent = '-';
                cell.appendChild(span);
            }
            table.appendChild(cell);
        }
    }

    renderCharts(foodData);
    renderSatisfactionTable(foodData);

    // Toggle between food and category statistics
    document.getElementById('toggle-food').addEventListener('click', function() {
        renderCharts(foodData);
        renderSatisfactionTable(foodData);
        this.classList.add('btn-dark');
        this.classList.remove('btn-outline-dark');
        document.getElementById('toggle-category').classList.remove('btn-dark');
        document.getElementById('toggle-category').classList.add('btn-outline-dark');
    });
    document.getElementById('toggle-category').addEventListener('click', function() {
        renderCharts(categoryData);
        renderSatisfactionTable(categoryData);
        this.classList.add('btn-dark');
        this.classList.remove('btn-outline-dark');
        document.getElementById('toggle-food').classList.remove('btn-dark');
        document.getElementById('toggle-food').classList.add('btn-outline-dark');
    });

    // Handle child selection to update statistics for the selected child
    document.querySelectorAll('input[name="child"]').forEach(radio => {
        radio.addEventListener('change', function() {
            window.location.href = '?child_id=' + this.value;
        });
    });
});