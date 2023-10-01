// Log Data and Options
var myChartElement = document.getElementById('myChart');
var data = JSON.parse(myChartElement.getAttribute('data-data'));
var options = JSON.parse(myChartElement.getAttribute('data-options'));

console.log('Data:', data);
console.log('Options:', options);

// Check if Chart is defined
if (typeof Chart === 'undefined') {
    console.error('Chart.js is not loaded');
} else {
    // Get the context of the canvas element we want to select
    var ctx = myChartElement.getContext('2d');
    
    // Create a new chart
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}
