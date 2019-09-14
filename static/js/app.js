function buildMetadata(state) {

  // Complete the function that builds the metadata panel housing state data

  // Use `d3.json` to fetch the metadata for a sample
  let metadataURL = "/metadata/" + state;
  // Use d3 to select the panel with id of `#state-metadata`
  let panelMetadata = d3.select("#state-metadata");
    // Use `.html("") to clear any existing metadata
    panelMetadata.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Use d3 to append new tags for each key-value in the metadata inside the loop.

    d3.json(metadataURL).then(function(data) {
      Object.entries(data).forEach(([key, value]) => {
        panelMetadata.append("p").text(`${key}: ${value}`)
        
        //console.log(`${key} ${value}`);
      });
    });
}

function buildCharts(state) {

  // Use `d3.json` to fetch the sample data for the plots
  let chartsURL = "/states/" + state;

  d3.json(chartsURL).then(function (data) {
    // CHART 1: Pie Chart, Injuries vs Fatalities
  })


}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/state").then((state) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
