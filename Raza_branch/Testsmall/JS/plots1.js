var plot1data = data;

var trace1 = {
  x: plot1data.map(row => row.state),
  y: plot1data.map(row => row.killed),
  name: "Killed",
  type: "bar"
};

var trace2 = {
  x: plot1data.map(row => row.state),
  y: plot1data.map(row => row.injured),
  name: "Injured",
  type: "bar"
};

// Combining both traces
var plot1chart = [trace1, trace2];

// Apply the group barmode to the layout
var layout = {
  title: "United States Gun Fatalities and Injuries",
  xaxis: { title: "State" },
  yaxis: { title: "Number Injured or Killed" },
  barmode: "group",
  hovermode: 'closest'
};

// Render the plot to the div tag with id "plot"
Plotly.newPlot("plot1chart", plot1chart, layout);