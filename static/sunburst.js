const unique = (value, index, self) => {
  return self.indexOf(value) === index
}
function createMap(data) {
  console.log(data);
  //code here for Map
  var types = ["Pets"];
  types = types.concat(data.map(x => x.type));
  var uniqueTypes = types.filter(unique);
  var uniqueTypes2 = data.map(x => x.type).filter(unique);
  var breeds = data.map(x => x.breeds.primary);
  var species = data.map(x => x.species);
  var uniqueSpecies = species.filter(unique);
  var colors = data.map(x => x.colors.primary);
  var age = data.map(x => x.age);
  var gender = data.map(x => x.gender);
  var sizes = data.map(x => {
      if (x.size=="Small") {
          return 1
      }
      else if (x.size=="Medium") {
          return 2
      }
      else if (x.size=="Large") {
          return 3
      }
      else if (x.size=="Extra Large") {
          return 4
      }
      else {
          return 0
      }
  });
  console.log(uniqueTypes);
  console.log(uniqueTypes2)
  
  var data1 = [{
      type: "sunburst",
      labels: uniqueTypes2,
      parents: uniqueTypes,
      values: [1,1,4,4,5,5,5,8,8],
      outsidetextfont: {size: 20, color: "#377eb8"},
      leaf: {opacity: 0.4},
      marker: {line: {width: 2}},
  }];

  var layout = {
      margin: {l: 0, r: 0, b: 0, t: 0},
      width: 500,
      height: 500
  };

  Plotly.newPlot('map', data1, layout);
}