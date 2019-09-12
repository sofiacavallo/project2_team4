function buildMetadata(sample) {
  var metadataSelector = d3.select('#sample-metadata');

  d3.json(`/metadata/${sample}`).then( data =>{
    metadataSelector.html("");
    console.log(Object.entries(data));
    Object.entries(data).forEach(([key,value]) =>{
      metadataSelector
        .append('p').text(`${key} : ${value}`)
        .append('hr')
    });
    })
}

function pieChart(data) {
    console.log(data);
    let labels = data.otu_ids.slice(0,10);
    let values = data.state_values.slice(0,10);
    let hovertext = data.otu_labels.slice(0,10);

    let trace = [{
      values : values,
      labels : labels,
      type : "pie",
      textposition: "inside",
      hovertext : hovertext
    }];

    let layout = {
        title: '<b> Gun Violence Pie Chart </b>',
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
    };

    Plotly.newPlot('pie', trace , layout, {responsive: true});
}

function hbar(data) {
  let x = data.otu_ids;
  let y = data.state_values;
  let markersize = data.state_values;
  let markercolors = data.otu_ids;
  let textvalues = data.otu_labels;

  let trace =[{
    x: x,
    y: y,
    mode: 'markers',
    marker: {
      size: markersize,
      color: markercolors,
    },
    text: textvalues
  }];

  let layout ={
    title:"<b> Gun Violence Bar Graph </b>",
    xaxis: {
      title: 'Deaths',
    },
    yaxis: {
      title: 'Cities'
    },
    width:1100,
    plot_bgcolor: 'rgba(0, 0, 0, 0)',
    paper_bgcolor: 'rgba(0, 0, 0, 0)',
  };

  Plotly.newPlot('hbar', trace, layout, {responsive: true});
}

function buildCharts(sample) {

  d3.json(`/samples/${sample}`).then( data =>{
    // ## Pie Chart ##
    pieChart(data);
    // ## Bubble Chart ##
    hbar(data);
  }); 
}
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
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
