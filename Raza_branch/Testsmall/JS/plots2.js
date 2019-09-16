var plot2data = data;

// Select the button
var button = d3.select("#button");

button.on("click", function() {

  // Select the text from the input field after the button click:
  var inputElement = d3.select("#State-form-input");
  var inputValue = inputElement.property("value");

  //Select the states that are the same as the state user selected
  var filteredData = plot2data.filter(value => value.state === inputValue);

  var trace1 = {
    x: filteredData.map(row => row.city_or_county),
    y: filteredData.map(row => row.killed),
    name: "Killed",
    type: "bar"
  };
  
  var trace2 = {
    x: filteredData.map(row => row.city_or_county),
    y: filteredData.map(row => row.injured),
    name: "Injured",
    type: "bar"
  };
  
  // Combining both traces
  var plot2chart = [trace1, trace2];
  
  // Apply the group barmode to the layout
  var plot2layout = {
    title: "Injuries and Fatalities per City",
    xaxis: { title: "City" },
    yaxis: { title: "Number Injured or Killed" },
    barmode: "group",
    hovermode: 'closest'
  };
  
  // Render the plot to the div tag with id "plot"
  Plotly.newPlot("plot2chart", plot2chart, plot2layout);

  // Create the Traces for plot 3: injuries vs fatalities per month
  var trace3 = {
    x: filteredData.map(row => row.date.split("-")[1]),
    y: filteredData.map(row => row.killed),
    type: "bar",
    name: "Fatalities",
  };
  
  var trace4 = {
    x: filteredData.map(row => row.date.split("-")[1]),
    y: filteredData.map(row => row.injured),
    type: "bar",
    name: "Injuries",
  };
  
  // Create the data array for the plot
  var plot3chart = [trace3, trace4];
  
  // Define the plot layout
  var plot3layout = {
    title: "Incidents per Month",
    xaxis: { title: "Month" },
    yaxis: { title: "Number Injured or Killed" },
    barmode: "group",
    hovermode: 'closest'
  };
  
  // Plot the chart to a div tag with id "plot"
  Plotly.newPlot("plot3chart", plot3chart, plot3layout);

  //Pie Chart of cities and sum of their incidents
  var trace5 = {
    labels: filteredData.map(row => row.city_or_county),
    values: filteredData.map(row => row.killed),
    type: 'pie'
  };

  var piedata = [trace5];

  var pielayout = {
    title: "Fatalities Per City",
  };

  Plotly.newPlot("piechart", piedata, pielayout);

  // Plot the chart to a div tag with id "plot"
  Plotly.newPlot("plot3chart", plot3chart, plot3layout);

  //Pie Chart of cities and sum of their incidents
  var trace6 = {
    labels: filteredData.map(row => row.city_or_county),
    values: filteredData.map(row => row.injured),
    type: 'pie'
  };

  var pie2data = [trace6];

  var pie2layout = {
    title: "Injuries Per City",
  };

  Plotly.newPlot("pie2chart", pie2data, pie2layout);

})
