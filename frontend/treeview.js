// responsible for setting up treeview using companies node data 
class TreeView {

  constructor(corporate_number) {
    
      this.myDiagram = null;  
      this.corporate_number = corporate_number;

      //data 
      this.jsonData = null; 
      this.csvData = null; 
  }

  init() {
      this.getNodeDataViaAPI().then(data => {
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
    this.myDiagram.findTreeRoots().each(r => r.expandTree(0));
  }
  
  // @Todo3 
  async getNodeDataViaAPI() {
    // make url 
    let base_url  = 'https://fdinzk1cn9.execute-api.ap-northeast-1.amazonaws.com/dev/fetchCompanyNodeData?corporate_number='
    const query_url = base_url  +  this.corporate_number; 
    console.log(query_url)
    let org_view_data = null; 

    
    try {
      const response = await fetch(query_url);
      console.log('received http full response : ')
      const data = await response.json();

      // extract from http response 
      org_view_data = data.body.org_view_data
      this.csvData = data.body.org_gsheet_data

      // show data use for display treeview 
      console.log('Node Data fetched:', org_view_data);  
    } 
  
    catch (error) {
        console.error('Error fetching data:', error);
    }

    // convert json string json object 
    return JSON.parse(org_view_data);
  
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

  expandByLevel(level,expandCollapseFlag) {
    if (expandCollapseFlag){
      this.myDiagram.findTreeRoots().each(r => r.expandTree(level));
    }
    else {
      this.myDiagram.findTreeRoots().each(r => r.collapseTree(level-1));
    }
     
  }

  // get csv data so user can copy and paste to google sheet 
  getCsvData(){
    return this.csvData
  }
   

}; // end of TreeView class 


/* 
=================================
Initialize tree view diagram 
=================================
*/

// global var 
let diagramObject; 
let expanseCollapseFlagArray = [true, true, true]; // expand/collapse all, e/c 事業部 , e/collapse 部 

document.addEventListener('DOMContentLoaded', () => {

});


/* 
=================================
Diagram functionalities
=================================
*/

// Function to change the company graph based on user 'business id' input  
function changeCompanyGraph() {
  // get corporate number from user input 
  const corporate_number = document.getElementById('corporate_number_input').value;

  // destroy previous 
  if (diagramObject) {
    diagramObject.destroy();
  }

  diagramObject = new TreeView(corporate_number);
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
var expandCollapseAllIndex = 0; 
diagramObject.toggleAllNodes(expanseCollapseFlagArray[expandCollapseAllIndex]); // initially true
expanseCollapseFlagArray[expandCollapseAllIndex] = !expanseCollapseFlagArray[expandCollapseAllIndex]; // Toggle the flag
}

function toggleExpandCollapselevel1() {
var expandCollapseAllIndex = 1;
diagramObject.expandByLevel(3,expanseCollapseFlagArray[expandCollapseAllIndex]) 
expanseCollapseFlagArray[expandCollapseAllIndex] = !expanseCollapseFlagArray[expandCollapseAllIndex]; 
} 

function toggleExpandCollapselevel2() {
var expandCollapseAllIndex = 2;
diagramObject.expandByLevel(4,expanseCollapseFlagArray[expandCollapseAllIndex]) 
expanseCollapseFlagArray[expandCollapseAllIndex] = !expanseCollapseFlagArray[expandCollapseAllIndex]; 
} 




function copyToClipboard() {
  const data = diagramObject.getCsvData()
  // Convert the data to a tab-delimited string
  let clipboardText = "headquarter\tdivision\tdepartment\tsection\tsite\n"; // Header row
  data.forEach(row => {
      clipboardText += `${row.headquarter}\t${row.division}\t${row.department}\t${row.section}\t${row.site}\n`;
  });

  // Create a temporary textarea element to hold the text
  const tempTextArea = document.createElement("textarea");
  tempTextArea.value = clipboardText;
  document.body.appendChild(tempTextArea);

  // Select the text and copy it to the clipboard
  tempTextArea.select();
  document.execCommand("copy");

  // Remove the temporary textarea
  document.body.removeChild(tempTextArea);

  alert("Data copied to clipboard. You can now paste it into Google Sheets.");
}

