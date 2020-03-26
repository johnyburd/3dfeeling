import React from 'react'
import { withRouter } from 'react-router-dom'
import './Details.scss'

import 'bootstrap/dist/css/bootstrap.min.css'

import Feelbar from './Feelbar'

class Details extends React.Component {

  componentDidMount() {
    console.log('Details Mounted')
  }

  render () {
    return (
        <div className="Details">
          <Feelbar />
          <div className="Details-header">
            <div className="Details-content">
              <h1>About 3D Feeling</h1>
              <ul>
                <li>
                  Our project, 3D Feeling, creates a 3D representation 
                  of emotions found within a corpus of text. 
                  This is not definitive, as extracting sentiment 
                  from a text corpus and modeling it in 3D space 
                  is an abstract problem that has no right answer. 
                  Our solution generates 3D models that have a 
                  quantitative and explainable foundation while 
                  also instilling complex, indescribable emotion in the viewer. 
                  We achieve this task by using information gathered 
                  from natural language processing data collection 
                  methods, which inspire a 3D model that can be 
                  built in the real world.
                </li>
                <br />
                <li>This project was built by a team of six 
                  Georgia Tech students for Dr. Krystin Gollihue. 
                  Dr. Gollihue is a Marion L. Brittain Postdoctoral Fellow 
                  at Georgia Tech, and the origin of this wonderful idea.
                </li>
                <br />
                <li>VAD Explanation</li>
                <br />
                <li>Classifier Methodology</li>
                <br />
                <li>Object Generation</li>
                <br />
                <li>Stuff for Nerds: Tools and technologies</li>
                <br />
              </ul>
              <p>(Put rights and licensing here)</p>
            </div>
          </div>
        </div>
    )
  }
}

export default withRouter(Details);
