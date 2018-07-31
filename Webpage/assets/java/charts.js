
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawVisualization);

      function drawVisualization(arraydata) {
        // Some raw data (not necessarily accurate)
        var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
      title : 'Battery 2nd Life Statistic',
      vAxis: {title: 'SoC'},
      hAxis: {title: 'Calendar Week'},
      seriesType: 'bars',
      series: {3: {type: 'line'},
			4: {type: 'line'},
			5: {type: 'line'}


			}

    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
    chart.draw(data, options);
    }
