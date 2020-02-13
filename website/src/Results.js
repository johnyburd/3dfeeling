import React from 'react'
import { withRouter } from 'react-router-dom'

import 'bootstrap/dist/css/bootstrap.min.css';

import { STLViewer } from 'react-stl-obj-viewer';

class Results extends React.Component {

  componentDidMount() {
    console.log('Results Mounted')
  }

  render () {
      return (
        <div className="Results">
          <div className="background">
            <div className='item'>
              <div className='Results-header'>
                <h2>This is your shape in all of its glory!</h2>
                <p>Analysis values and the text it was generated from are below.</p>
                <STLViewer
                  url={'https://api.3dfeeling.ga/assets/' + this.props.location.state.apiFileName}
                  sceneClassName="test-scene"
                  modelColor='red'
                />
                <p>Average Values:</p>
                <ul>
                  <li>
                    Valence: { this.props.location.state.valence }
                  </li>
                  <li>
                    Arousal: { this.props.location.state.arousal }
                  </li>
                  <li>
                    Dominance: { this.props.location.state.dominance }
                  </li>
                </ul>
                <p>Input text: { this.props.location.state.inputText }</p>
              </div>
            </div>
          </div>
        </div>
      )
    }
}

export default withRouter(Results);
