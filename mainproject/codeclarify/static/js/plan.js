

document.addEventListener('DOMContentLoaded', function () {
    
        const ctx = document.getElementById('weightChart').getContext('2d');
        
        const weeks =document.getElementById('weeks').innerHTML;
        const weights = document.getElementById('weights').innerHTML;
        
        
    const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: weeks,
                datasets: [{
                    label: 'Weight Gain Progress',
                    data: weights,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false,
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    },
                    y: {
                        min: 0,
                    }
                }
            }
        });
      });
   