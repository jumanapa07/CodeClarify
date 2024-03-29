console.log('Weight.js is running');

document.addEventListener('DOMContentLoaded', function () {
const table = document.getElementById('weightable');

let recorded_weight = [];
let recorded_date = [];

for (let i = 1; i < table.rows.length; i++) {
  recorded_weight.push(parseFloat(table.rows[i].cells[0].textContent));
  recorded_date.push(table.rows[i].cells[1].textContent);
}

let values = recorded_weight.flat();
console.log(recorded_weight);
console.log(recorded_date);
console.log(values);


// Set new default font family and font color to mimic Bootstrap's default styling
// Chart.defaults.global.defaultFontFamily =
//   'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
// Chart.defaults.global.defaultFontColor = '#858796';

// Area Chart - Weight History
const ctxAreaChart = document.getElementById('myChart').getContext('2d');
const myAreaChart = new Chart(ctxAreaChart, {
  type: 'line',
  data: {
    labels: [...recorded_date],
    datasets: [
      {
        label: 'Weight',
        data: values,
        lineTension: 0.3,
       backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1,
        pointRadius: 5,
        pointBackgroundColor: 'rgba(2,117,216,1)',
        pointBorderColor: 'rgba(255,255,255,0.8)',
        pointHoverRadius: 5,
        pointHoverBackgroundColor: 'rgba(2,117,216,1)',
        pointHitRadius: 50,
        pointBorderWidth: 2,
      },
    ],
  },
  options: {
    scales: {
      xAxes: [
        {
          ticks: {
            autoSkip: false,
            maxRotation: 60,
            minRotation: 60,
          },
          gridLines: {
            display: true,
          },
          scaleLabel: {
            display: true,
            padding: 10,
            fontColor: '#555759',
            fontSize: 16,
            fontStyle: 700,
            labelString: 'Date',
          },
        },
      ],
      yAxes: [
        {
          ticks: {
            min: 0,
            max: 120,
            maxTicksLimit: 12,
            padding: 10,
            // Include a 'kg' in the ticks
            callback: function (value, index, values) {
              return value + 'kg';
            },
          },
          gridLines: {
            color: 'rgba(0, 0, 0, .125)',
          },
          scaleLabel: {
            display: true,
            padding: 10,
            fontColor: '#555759',
            fontSize: 16,
            fontStyle: 700,
            labelString: 'Weight in kg',
          },
        },
      ],
    },
    legend: {
      display: false,
    },
  },
});
});