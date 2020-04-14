//var nodes = new vis.DataSet([
//    {id: 1, label: 'Node 1'},
//    {id: 2, label: 'Node 2'},
//    {id: 3, label: 'Node 3'},
//    {id: 4, label: 'Node 4'},
//    {id: 5, label: 'Node 5'}
//  ]);
//

var nodes_lst = []
var edges_lst = []
var i = 1;
var j;
var key_len;

nodes_lst.push({id: 1, label: data['querry'], link: ""});

var results = data["results"]
for (key in results){

    nodes_lst.push({id: 10 + i, label: key, link: ""});
    edges_lst.push({id: 10 + i, from: 1, to: 10 + i});
    j = 1;
    for (name in data["results"][key]){
        nodes_lst.push({id: 100 * i + j, label: name, link: data["results"][key][name]});
        edges_lst.push({id: 100 * i + j, from: 10+i, to: 100*i + j});
        j += 1;
    }
    i += 1;

}




//for (i=0; i < results.length; i++){
//    nodes_lst.push({id: i + 1, label: results[i]})
//}
var nodes = new vis.DataSet(nodes_lst)
var edges = new vis.DataSet(edges_lst)
  // create an array with edges
//  var edges = new vis.DataSet([
//    {from: 1, to: 3},
//    {from: 1, to: 2},
//    {from: 2, to: 4},
//    {from: 2, to: 5},
//    {from: 3, to: 3}
//  ]);

  // create a network



  var container = document.getElementById('mynetwork');
  var node_data = {
    nodes: nodes,
    edges: edges
  };
 var options = {
  clickToUse: true,
  layout: {
    improvedLayout:true,
    hierarchical: {
      enabled:false,
      levelSeparation: 150,
      nodeSpacing: 100,
      treeSpacing: 200,
      blockShifting: false,
      edgeMinimization: false,
      parentCentralization: true,
      direction: 'LR',        // UD, DU, LR, RL
      sortMethod: 'directed',  // hubsize, directed
      shakeTowards: 'leaves'  // roots, leaves
    }
  }
}


var i = 1;
var j;
var key_len;

var nodeID = node_data.nodes.get(1);
nodeID.color = {border: '#00ff00', background: '#00ff00', highlight: {border: '#00ff00', background: '#00ff00'}}
nodes.update(nodeID);


for (key in results){
    var nodeID = node_data.nodes.get(10 + i);
    nodeID.color = {border: '#0000ff', background: '#0000ff', highlight: {border: '#0000ff', background: '#0000ff'}}
    nodes.update(nodeID);
    j = 1;
     for (name in data["results"][key]){
        var nodeID = node_data.nodes.get(100 * i + j);
        nodeID.color = {border: '#ff0000', background: '#ff0000', highlight: {border: '#ff0000', background: '#ff0000'}}
        nodes.update(nodeID);
        j += 1;
     }
     i += 1;
}


  var network = new vis.Network(container, node_data, options);
  network.on('click', function(obj){
  nodeId = obj.nodes[0];      // the node id that getNodeAt() should be returning
  if (nodeId > 100){
  node = nodes.get(nodeId);
  $("#preview").html('<object style="height:100%; width:40%;" data="/node_decode/'+node.link+'"/>');
  }

});