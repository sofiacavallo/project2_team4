// // Submit Button handler
// function handleSubmit() {
//   // Prevent the page from refreshing
//   d3.event.preventDefault();

//   // Select the input value from the form
//   var state = d3.select("#stateInput").node().value;
//   console.log(state);

//   // clear the input value
//   d3.select("#stateInput").node().value = "";

//   // Build the plot with the new stock
//   buildPlot(state);
// }


// function buildPlot(state) {
//   Plotly.d3.json('Datasets/gunviolence_db.json').then(function(data) {

//     // Grab values from the response json object to build the plots
//     var date = data.dataset.Incident_Date;
//     var year = data.dataset.year;
//     var stat = data.dataset.State;
//     var city = data.dataset.City_Or_County;
//     var numberkilled = data.dataset.Number_Killed;
//     var numberinjured = data.dataset.Number_Injured;

//     var trace1 = {
//       type: "scatter",
//       mode: "lines",
//       name: stat,
//       x: city,
//       y: numberkilled,
//       line: {
//         color: "#17BECF"
//       }
//     };

//     var data = [trace1];

//     var layout = {
//       title: `${Stat} Gun Violence Stats`,
//         yaxis: {
//         autorange: true,
//         type: "linear"
//       }
//     };

//     Plotly.newPlot("plot", data, layout);

//   });
// }

// // Add event listener for submit button
// d3.select("#submit").on("click", handleSubmit);


// Trace1 for the  Data
// var trace1 = {
//   x: data.map(row => row("State")),
//   y: data.map(row => row("Number_Killed")),
//   name: "State",
//   type: "bar"
// };

// // Combining both traces
// var data = [trace1];

// // Apply the group barmode to the layout
// var layout = {
//   title: "Number Killed per State",
// };

// // Render the plot to the div tag with id "plot"
// Plotly.newPlot("plot", data, layout);

// data.forEach((incident) => {
//   console.log(incident);

//   // Get the entries for each object in the array
//   Object.entries(user).forEach(([key, value]) => {
//     // Log the key and value
//     console.log(`Key: ${key} and Value ${value}`);
//   });
// });










// // Create empty arrays to store the dish and spice values
// var allstates = [];

// // Iterate through each recipe object
// data.forEach((state) => {

//   // Iterate through each key and value
//   Object.entries(state).forEach(([key, value]) => {

//     // Use the key to determine which array to push the value to
//     if (key === "state") {
//       allstates.push(value);
//     }
//    });
// });

// console.log(allstates)
// allstates = allstates.map(el => el.trim());
// var states = [... new Set(allstates)];
// console.log(states)






// // Insert list of states that are in this view:
// var str = '<ul>'
// states.forEach(function(state) {
//   str += '<li>'+ state + '</li>';
// }); 
// str += '</ul>';
// document.getElementById("slideContainer").innerHTML = str;



// // Assign the data from `data.js` to a descriptive variable
// var dataxyz = data;
// // Select the button
// var button = d3.select("#button");

// button.on("click", function() {

//   // Select the input element and get the raw HTML node
//   var inputElement = d3.select("#patient-form-input");

//   // Get the value property of the input element
//   var inputValue = inputElement.property("value");

//   console.log(inputValue);

//   var filteredData = dataxyz.filter(person => person.State === (inputValue));

//   console.log(filteredData);

//   var Injured = filteredData.map(person => person.Number_Injured);
//   console.log(Injured);
//   var sum = math.sum(Injured);
//   console.log(sum);
//  var mean = math.mean(...Injured);
//  console.log(mean);
  // var median = math.median(ages);
  // var mode = math.mode(ages);
  // var variance = math.var(ages);
  // var standardDeviation = math.std(ages);

  // // Then, select the unordered list element by class name
  // var list = d3.select(".summary");

  // // remove any children from the list to
  // list.html("");

  // // append stats to the list
  // list.append("li").text(`Mean: ${mean}`);
  // list.append("li").text(`Median: ${median}`);
  // list.append("li").text(`Mode: ${mode}`);
  // list.append("li").text(`Variance: ${variance}`);
  // list.append("li").text(`Standard Deviation: ${standardDeviation}`);
});
