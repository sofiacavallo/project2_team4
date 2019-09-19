function buildMetadata(state) {

  // Complete the function that builds the metadata panel housing state data

  // Use `d3.json` to fetch the metadata for a sample
  let metadataURL = "/metadata/" + state;
  // Use d3 to select the panel with id of `#state-metadata`
  let panelMetadata = d3.select("#gunviolence_metadata");
    // Use `.html("") to clear any existing metadata
    panelMetadata.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Use d3 to append new tags for each key-value in the metadata inside the loop.

    d3.json(metadataURL).then(function(data) {
      console.log(Object.entries(data));
      Object.entries(data).forEach(([key, value]) => {
        panelMetadata.append("p").text(`${key}: ${value}`)
        
        //console.log(`${key} ${value}`);
      });
    });
};


function barChart(data) {
  console.log(data.number_killed);
  let trace1 = {
    x: data.cities_or_counties,
    y: data.number_killed,
    name: "Killed",
    type: "bar"
  };
  
  let trace2 = {
    x: data.cities_or_counties,
    y: data.number_injured,
    name: "Injured",
    type: "bar"
  };
  
  // Combining both traces
  let plot2chart = [trace1, trace2];
  
  // Apply the group barmode to the layout
  let plot2layout = {
    title: "Injuries and Fatalities per City",
    xaxis: { title: "City" },
    yaxis: { title: "Number Injured or Killed" },
    barmode: "group",
    hovermode: 'closest'
  };
  
  // Render the plot to the div tag with id "plot"
  Plotly.newPlot("plot2chart", plot2chart, plot2layout);

};

// //Still working on this one -MRR
// function barChart2(data) {
//   let trace3 = {
//     x: filteredData.map(row => row.date.split("-")[1]),
//     y: filteredData.map(row => row.killed),
//     type: "bar",
//     name: "Fatalities",
//   };

//   var trace4 = {
//     x: filteredData.map(row => row.date.split("-")[1]),
//     y: filteredData.map(row => row.injured),
//     type: "bar",
//     name: "Injuries",
//   };

//   // Create the data array for the plot
//   var plot3chart = [trace3, trace4];

//   // Define the plot layout
//   var plot3layout = {
//     title: "Incidents per Month",
//     xaxis: { title: "Month" },
//     yaxis: { title: "Number Injured or Killed" },
//     barmode: "group",
//     hovermode: 'closest'
//   };

//   // Plot the chart to a div tag with id "plot"
//   Plotly.newPlot("plot3chart", plot3chart, plot3layout);
// }

function piechart1(data) {
  let trace5 = {
    labels: data.cities_or_counties,
    values: (data.number_killed > 0 ),
    type: 'pie'
  };

  let piedata = [trace5];

  let pielayout = {
    title: "Fatalities Per City",
  };

  Plotly.newPlot("piechart", piedata, pielayout);
};

function piechart2(data) {

  //Pie Chart of cities and sum of their incidents
  var trace6 = {
    labels: data.cities_or_counties,
    values: (data.number_injured > 0 ),
    type: 'pie'
  };

  var pie2data = [trace6];

  var pie2layout = {
    title: "Injuries Per City",
  };

  Plotly.newPlot("pie2chart", pie2data, pie2layout);
};

// //Still working on this too -MRR
// function fullchart(data) {
//   var trace11 = {
//     x: plot1data.map(row => row.state),
//     y: plot1data.map(row => row.killed),
//     name: "Killed",
//     type: "bar"
//   };
  
//   var trace12 = {
//     x: plot1data.map(row => row.state),
//     y: plot1data.map(row => row.injured),
//     name: "Injured",
//     type: "bar"
//   };
  
//   // Combining both traces
//   var plot11chart = [trace11, trace12];
  
//   // Apply the group barmode to the layout
//   var layout11 = {
//     title: "United States Gun Fatalities and Injuries",
//     xaxis: { title: "State" },
//     yaxis: { title: "Number Injured or Killed" },
//     barmode: "group",
//     hovermode: 'closest'
//   };
  
//   // Render the plot to the div tag with id "plot"
//   Plotly.newPlot("plot1chart", plot11chart, layout11);
// }

function buildCharts(state) {

  // Use `d3.json` to fetch the sample data for the plots
  let chartsURL = "/states/" + state;

  d3.json(chartsURL).then(function (data) {
    console.log(data);
    barChart(data);
    piechart1(data);
    piechart2(data);
  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#list_states");

  // Use the list of sample names to populate the select options
  d3.json("/states").then((state) => {
    state.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstState = state[0];
    buildCharts(firstState);
    buildMetadata(firstState);
  });
};

function optionChanged(newState) {
  // Fetch new data each time a new sample is selected
  buildCharts(newState);
  buildMetadata(newState);
};

// Initialize the dashboard
init();
