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
            <div className="Details-content">
              <p>This is the details page. You made it. Yay!</p>
            </div>
        </div>
    )
  }
}

export default withRouter(Details);
