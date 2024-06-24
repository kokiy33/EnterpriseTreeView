// responsible for setting up treeview using companies node data 
class TreeView {

    constructor(graphFile) {
        this.myDiagram = null; 
        this.graphFile = graphFile;
        this.jsonData = null;  
    }
  
    init() {
        this.fetchJsonData().then(data => {
          this.jsonData = data;
          this.setupDiagram();
        });
    }
    
    // Set up the chart 
    setupDiagram() {

      const $ = go.GraphObject.make; // to create various go js element
      this.myDiagram = new go.Diagram('myDiagramDiv', {
        allowMove: false,
        allowCopy: false,
        allowDelete: false,
        allowHorizontalScroll: false,
        layout: $(go.TreeLayout, {
          alignment: go.TreeAlignment.Start,
          angle: 0,
          compaction: go.TreeCompaction.None,
          layerSpacing: 16,
          layerSpacingParentOverlap: 1,
          nodeIndentPastParent: 1.0,
          nodeSpacing: 0,
          setsPortSpot: false,
          setsChildPortSpot: false,
        }),
      }); // end of creating new instance 


      this.myDiagram.nodeTemplate = $(go.Node,
        {
          // no Adornment: instead change panel background color by binding to Node.isSelected
          selectionAdorned: false,

          // a custom function to allow expanding/collapsing on double-click
          // this uses similar logic to a TreeExpanderButton
          doubleClick: (e, node) => {
            var cmd = this.myDiagram.commandHandler;
            if (node.isTreeExpanded) {
              if (!cmd.canCollapseTree(node)) return;
            } else {
              if (!cmd.canExpandTree(node)) return;
            }
            e.handled = true;
            if (node.isTreeExpanded) {
              cmd.collapseTree(node);
            } else {
              cmd.expandTree(node);
            }
          },
        },
        
        // Ensure all nodes are initially collapsed 
        {isTreeExpanded: false},
        
        // TreeExpanderButton
        $('TreeExpanderButton', {
          // customize the button's appearance
          _treeExpandedFigure: 'LineDown',
          _treeCollapsedFigure: 'LineRight',
          'ButtonBorder.fill': 'whitesmoke',
          'ButtonBorder.stroke': null,
          _buttonFillOver: 'rgba(0,128,255,0.25)',
          _buttonStrokeOver: null,
        }),


        $(go.Panel,
          'Horizontal',
          { position: new go.Point(18, 0) },
          new go.Binding('background', 'isSelected', (s) => (s ? 'lightblue' : 'white')).ofObject(),
          $(go.Picture,
            {
              width: 18,
              height: 18,
              margin: new go.Margin(0, 4, 0, 0),
              imageStretch: go.ImageStretch.Uniform,
            },
            // bind the picture source on two properties of the Node
            // to display open folder, closed folder, or document
            //new go.Binding('source', 'isTreeExpanded', imageConverter).ofObject(),
            // new go.Binding('source', 'isTreeLeaf', imageConverter).ofObject()
          ),
          $(go.TextBlock, { font: '9pt Verdana, sans-serif' }, new go.Binding('text', 'name'))
        ) // end Horizontal Panel
      ) // end of nodeTemplate ;
      
      this.myDiagram.model = new go.TreeModel(this.jsonData);

      // without lines 
      this.myDiagram.linkTemplate = $(go.Link);
      // 
      // this.myDiagram.findTreeRoots().each(r => r.expandTree(0));
    }
    
    // parse json data 
    fetchJsonData() {
      // HTTP get request 
      return fetch(this.graphFile, {
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      })
      // response handling 
      .then(response => response.json());
    }

    // destroy tree view instance (use for switching tree view for other companies)
    destroy() {
      if (this.myDiagram) {
        this.myDiagram.div = null; // This effectively removes the diagram from the DOM
        this.myDiagram.clear(); // Clear all nodes and links
        this.myDiagram = null; // Remove reference to the diagram
      }
    }
    // zoom node based on 'name' in postgraph node json file  
    zoomNode(NodeName){
      const firstNode = this.myDiagram.findNodesByExample({name: NodeName}).first();
      // focus on the query node 
      this.myDiagram.scale = 1;
      this.myDiagram.commandHandler.scrollToPart(firstNode);
    }

    // can expand and collapse all nodes.
    // parameter : true -> expand all, otherwise collapse all 
    toggleAllNodes(expand) {
      this.myDiagram.nodes.each(node => {
          if (expand) {
              this.myDiagram.commandHandler.expandTree(node);
          } else {
              this.myDiagram.commandHandler.collapseTree(node);
          }
      });
  }

}; // end of TreeView class 


// global var 
let diagramObject; 
let expandCollapseFlag = true; 

document.addEventListener('DOMContentLoaded', () => {
  diagramObject  = new TreeView("3180301014273.json");
  diagramObject.init();
});

// Function to change the company graph based on user 'business id' input  
function changeCompanyGraph() {
  // get corporate number from user input 
  const newGraphFile = document.getElementById('corporate_number_input').value + ".json";
  
  // destroy previous 
  if (diagramObject) {
    diagramObject.destroy();
  }
  
  diagramObject = new TreeView(newGraphFile);
  diagramObject.init();
}

// zoom node based on user input 
function userZoomNode(){
  // get user string 
  var userNodeName = document.getElementById("zoomNode").value; 
  diagramObject.zoomNode(userNodeName); 
}

// expandCollapse 
function userToggleAllNodes() {
  diagramObject.toggleAllNodes(expandCollapseFlag); // initially true
  expandCollapseFlag = !expandCollapseFlag; // Toggle the flag
}

  
  
  