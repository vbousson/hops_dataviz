document.addEventListener('DOMContentLoaded', function(){
  fetch('./data2.json')
    .then(resp => resp.json())
    .then(data => {
      console.log(JSON.stringify(data));
      var cy = window.cy = cytoscape({
        container: document.getElementById('cy'),
        autounselectify: true,					
        boxSelectionEnabled: false,
        layout: { name: 'cola' },
        style: [
          {
            selector: 'node',
            css: {
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
        elements: data
      });
    })
    .catch(() => alert('oh no!'));
});
