document.addEventListener('DOMContentLoaded', function(){
  fetch('/graph.json')
    .then(resp => resp.json())
    .then(data => {
      console.log(JSON.stringify(data));
      var cy = window.cy = cytoscape({
        container: document.getElementById('cy'),
        autounselectify: true,					
        boxSelectionEnabled: false,
        layout: { 
          name: 'cola',
          infinite: true
        },
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(id)',
              'background-color': '#faf'
            }
          },
          {
            selector: 'edge',
            css: {
              'line-color': '#f92411'
            }
          }
        ],
        elements: data,
        zoomingEnabled: true
      });
    })
    .catch(() => alert('oh no!'));    
});
