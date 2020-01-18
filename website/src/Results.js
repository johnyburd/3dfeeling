
import React from 'react';
import './Results.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import STLViewer from 'stl-viewer';

// Test model? 'https://bohdanbirdie.github.io/stl-obj-demo/bottle.stl'
import testSTL from './testSTL.stl'

class Results extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      resultText: 'Dummy Text. I haven\'t changed yet.',
    }
    this.updateText = this.updateText.bind(this)
  }

  updateText(newText) {
    this.setState({
      resultText: newText
    })
  }

  render () {
    return (
      <div className="Results">
        <div className="Background">
          <div className='item'>
            <div className='Results-header'>
              Results and shape will be displayed here
              <STLViewer
                model={testSTL}
                width={400}
                height={400}
                modelColor='#EAEAEA'
                backgroundColor='#222222'
                rotate={true}
                orbitControls={true}
              />
            <p>{this.state.resultText}</p>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Results;
