// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var result = null;
var xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET", "/static/prediction.txt", true);
// if (xmlhttp.status==200) {
//     result = xmlhttp.responseText;
// }
xmlhttp.onload = function() { 
  if (xmlhttp.status == 200) {
    result = xmlhttp.responseText;
    var lines = result.split("\n");
    prices = lines[0].split(" ");
    dates = lines[1].split(" ");

    // Area Chart Example
    var ctx = document.getElementById("line");

    // ctx.width = '200px';
    // ctx.height = '200px';
    var line = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [{
          label: "Price ($)",
          lineTension: false,
          fill: false,
          backgroundColor: "white",
          borderColor: "white",
          pointRadius: 7,
          pointBackgroundColor: "white",
          pointBorderColor: "rgba(29, 159, 59, 0.8)",
          pointHoverRadius: 10,
          pointHoverBackgroundColor: "white",
          pointHitRadius: 50,
          pointBorderWidth: 2,
    
          data: prices,
        }]
      }
    });
    // ctx.width = '200px';
    // ctx.height = '200px';
  } 
};
xmlhttp.send();