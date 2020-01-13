
import React from 'react';
import './Results.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import STLViewer from 'stl-viewer';

// Test model? 'https://bohdanbirdie.github.io/stl-obj-demo/bottle.stl'
import testSTL from './testSTL.stl'

function Results() {
  return (
    <div className="Results">
      <header className="Results-header">
        <div className="Results-display">
        Results and shape will be displayed here
        </div>
        <div>
        <STLViewer
        	model={testSTL}
        	width={400}
        	height={400}
        	modelColor='#EAEAEA'
        	backgroundColor='#222222'
        	rotate={true}
        	orbitControls={true}
        />
        </div>
      </header>
    </div>
  );
}

export default Results;
