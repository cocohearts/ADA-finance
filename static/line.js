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
    var line = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [{
          label: "Price ($)",
          lineTension: false,
          fill: false,
          backgroundColor: "rgba(2,117,216,1)",
          borderColor: "rgba(2,117,216,1)",
          pointRadius: 10,
          pointBackgroundColor: "rgba(2,117,216,1)",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 10,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 50,
          pointBorderWidth: 2,
    
          data: prices,
        }]
      }
    });
  } 
};
xmlhttp.send();