import React from 'react'
import { withRouter } from 'react-router-dom'
import './Results.scss'

import 'bootstrap/dist/css/bootstrap.min.css';

import { Image, Button, Form } from 'react-bootstrap';
import { STLViewer } from 'react-stl-obj-viewer';
import useDarkMode from 'use-dark-mode';

import Feelbar from './Feelbar'
import history from './history'

const ViewWithTheme = (name) => {
  const { value } = useDarkMode()

  const [dimensions, setDimensions] = React.useState({
    width: window.innerWidth
  })
  React.useEffect(() => {
    function handleResize() {
      if (window.innerWidth % 5 === 0) {
        setDimensions({
          width: window.innerWidth
        })
      }
    }

    window.addEventListener('resize', handleResize)
    return _ => {
      window.removeEventListener('resize', handleResize)
    }
  })
  console.log(value ? "#2d2d2d" : "#f6f8f9")
  return <STLViewer
    url={ 'https://api.3dfeeling.ga/assets/' + name.name }
    width={ dimensions.width / 2.3 }
    height={ dimensions.width / 2.6 }
    backgroundColor={ value ? "#2d2d2d" : "#f6f8f9" }
    sceneClassName={ value ? "#2d2d2d" : "#f6f8f9" }
    modelColor='#e6584d'
  />
}

class Results extends React.Component {

  componentDidMount() {
    console.log('Results Mounted')
    console.log('Location', this.props.location)
  }

  render () {
    //console.log(this.DarkModeStatus());
    if (this.props.location.state == null) {
      return (
        <div>
          <Feelbar />
          <div className="Error">
            <h1>Results have not been generated yet.</h1>
            <h1>Please return to the homepage using buttons above.</h1>
          </div>
        </div>
      )
    } else {
      return (
        <div className="Results">
          <Feelbar />
          <div>
            <div className='Results-header'>
              <div className="container">
                <div className="left-side">
                  <ViewWithTheme
                    name={this.props.location.state.apiFileName}
                  />
                  <div>
                    <Button
                      variant="success"
                      size='lg'
                      onClick={() => { window.location.href = "https://api.3dfeeling.ga/assets/" + this.props.location.state.apiFileName}}
                    >Download</Button>
                    <Button 
                      variant="primary" 
                      size='lg'
                      onClick={() => history.push({pathname: '/details'})}
                    >Details</Button>

                  </div>
                </div>
                <div className="right-side">
                  <Image
                    src={'https://api.3dfeeling.ga/assets/' + this.props.location.state.apiFileName.replace('stl', 'png')}
                    className="graph"/>
                  <Form>
                    <Form.Control
                        disabled={ true }
                        className="input-text"
                        //onChange={() => this.handleText(this.textInput.value)}
                        as="textarea"
                        size="lg"
                        rows="6"
                        defaultValue={this.props.location.state.inputText}
                      />
                  </Form>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    }
  }
}

export default withRouter(Results);
