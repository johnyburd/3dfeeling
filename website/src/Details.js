import React from 'react'
import { withRouter } from 'react-router-dom'

import 'bootstrap/dist/css/bootstrap.min.css';

import Feelbar from './Feelbar'

class Details extends React.Component {

  componentDidMount() {
    console.log('Details Mounted')
  }

  render () {
    return (
        <div>
            <Feelbar />
            <p>This is the details page. You made it. Yay!</p>
        </div>
    )
  }
}

export default withRouter(Details);
