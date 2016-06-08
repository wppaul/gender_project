       function drawChartAvgIncome{
        var dataInput = [['crime tweets per 100 ppl', 'average Income']];
        var xMin = 0;
        var xMax = 0;
        var yMin = 0;
        var yMax = 0;

        for (var i = 0; i < population.length; i++){
          给 x, y赋值对就的 suburb_boundaries里的population和income, 或找你对应的要比较的值
          var x = Number(population[i]);
          var y = Number(income[i]);

        这是用来限定x, y轴的范围， 可以直接给xMax, xMin, yMax, yMin值来限定
<!--           xMax = (x > xMax ? x : xMax);
          xMim = (x < xMin ? x : xMin);
          yMax = (y > yMax ? y : yMax);
          yMim = (y < yMin ? y : yMin);
          var singleLine = [x, y]; -->
          if (singleLine.indexOf(Math.log(-1)) == -1 && singleLine.indexOf(Math.log(0)) == -1 ){
            dataInput.push(singleLine);
          }
        }
        drawChart('Average Income', dataInput, xMax, xMin, yMax, yMin, "#6a51a3");
    }



    function drawChart(chartTitle, dataSet, xMax, xMin, yMax, yMin, colorCode) {
        var data = google.visualization.arrayToDataTable(dataSet);

        var options = {
          title: chartTitle,
          hAxis: {title: dataSet[0][0] ,minValue: xMin, maxValue: xMax},
          vAxis: {title: dataSet[0][1] ,minValue: yMin, maxValue: yMax},
          chartArea: {width:'65%'},
          trendlines: {
            0: {
              type: 'linear',
              degree: 2,
              visibleInLegend: true
            }
          }
        };
        options.colors = [colorCode];

        var chartExponential = new google.visualization.ScatterChart(document.getElementById("container1"));
        chartExponential.draw(data, options);
    }
