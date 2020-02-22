import React from 'react'
import { withRouter } from 'react-router-dom'
import './App.scss'

import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.min.css'

import { Form, Button } from 'react-bootstrap';
import DarkModeToggle from './Dark';
import Loader from 'react-loader-spinner';


class App extends React.Component {
  constructor(props) {
    super(props)

    //State of the entire app since it is all being rendered through one large component
    this.state = {
      inputText: '',
      loading: false,
      inputFile: null,
    }

    this.fileName = ""

    //This allows react components to use their methods within the class. Don't ask me why
    this.handleText = this.handleText.bind(this)
    this.sendTextToAPI = this.sendTextToAPI.bind(this)
    this.pointsAverage = this.pointsAverage.bind(this)
    this.handleFile = this.handleFile.bind(this)
    this.sendFileToAPI = this.sendFileToAPI.bind(this)
    this.resetState = this.resetState.bind(this)
  }

  //Called whenever the component mounts before rendering. (Startup)
  componentDidMount() {
    console.log('Component Mounted')
  }

  //Responsible for updating state when contents of textbox change
  handleText(newText) {
    this.setState({
      inputText: newText,
    })
  }

  //Updates state when file is uploaded
  handleFile(newFile) {
    // Simply store file as Form Data. Use this if gonna send file to API
    console.log(newFile)
    if (newFile) {
      let file = new FormData()
      file.append('file', newFile)
      this.fileName = newFile.name
      this.setState({
        inputFile: file
      })
    }
  }

  //Clears state of app which rerenders inital page
  resetState() {
    this.setState({
      inputText: '',
      loading: false,
      inputFile: null,
    })
  }

  //Averages points returned from API. Not fail safe yet
  pointsAverage(points) {
    let averages = [0, 0, 0]
    let num = points.length
    for (let i = 0; i < num; i++) {
      averages[0] += points[i][0]
      averages[1] += points[i][1]
      averages[2] += points[i][2]
    }
    averages[0] /= num
    averages[1] /= num
    averages[2] /= num
    console.log("Averages of points: " + averages)
    return averages
  }

  //Sends form data stored in state to API
  sendFileToAPI() {
    let currentComponent = this
    let retrievedData = {
      apiFileName: "Didnt work",
      points: [[-1, -1, -1]],
    }
    console.log('File params', this.state.inputFile)
    this.setState({
      loading: true
    })
    axios.post('https://api.3dfeeling.ga/analyze-file',
      this.state.inputFile,
      {
        'Content-Type': 'multipart/form-data'
      }
    ).then(function (resp) {
      console.log(resp)
      //Assign gathered sentiment analysis values here
      retrievedData = resp.data
      let averages = currentComponent.pointsAverage(retrievedData.points)
      if (currentComponent.state.loading) {
        currentComponent.setState({
          loading: false,
        })
        currentComponent.props.history.push({
          pathname: '/results',
          state: {
            inputText: retrievedData.text,
            valence: averages[0],
            arousal: averages[1],
            dominance: averages[2],
            apiFileName: retrievedData.filename,
          }
        })
      }
      console.log(retrievedData)
    }).catch(function (error) {
      console.log(error)
      currentComponent.props.history.push({
        pathname: '/results',
        state: {
          inputText: "error reading text",
          valence: 0,
          arousal: 0,
          dominance: 0,
          apiFileName: 'unknown',
        }
      })
    });
  }

  //Sends input text from textbox to API
  sendTextToAPI() {
    let currentComponent = this
    let retrievedData = {
      apiFileName: "Didnt work",
      points: [[-1, -1, -1]],
    }
    console.log('Input text: ', this.state.inputText)
    const text = this.state.inputText
    console.log(text)
    this.setState({
      loading: true
    })
    axios.post('https://api.3dfeeling.ga/analyze',
      `text=${this.state.inputText}`
    ).then(function (resp) {
      console.log(resp)
      //Assign gathered sentiment analysis values here
      retrievedData = resp.data
      let averages = currentComponent.pointsAverage(retrievedData.points)
      if (currentComponent.state.loading) {
        currentComponent.setState({
          loading: false,
        })
        currentComponent.props.history.push({
          pathname: '/results',
          state: {
            inputText: currentComponent.state.inputText,
            valence: averages[0],
            arousal: averages[1],
            dominance: averages[2],
            apiFileName: retrievedData.filename,
          }
        })
      }
      console.log(retrievedData)
    }).catch(function (error) {
      console.log(error)
    });
  }

  /**
   * Renders the entire app.
   *
   * Called after the component mounts,
   *  or every time the app's state changes
   *
   * Right now it's just a conditional render:
   * App renders different things based on variables
   *  that are changed when certain things happen
   *
   * 1st: Input page (loading and loaded are false)
   * 2nd: Loading page (loading is true, loaded is still false)
   * 3rd: Results page (loading is false and loaded is true)
  **/
  render () {
    if (!this.state.loading) {
      return (
        <div>
          <DarkModeToggle/>
          <div className="App">
            <div>
              <Form onSubmit={this.state.inputFile ? this.sendFileToAPI : this.sendTextToAPI}>
              <Form.Label className="mb-5">
                <p><strong>3D Feeling</strong> is a project designed to help you model emotions.</p>
                <p>The app will process text and produce a 3D representation of the emotions from the text.</p>
                <br/>
                <strong>Enter text in the input box or upload a file to get started.</strong>
                <br/>
              </Form.Label>
                <div className="container-c">
                  <div className="item Textarea">
                    <Form.Group controlId="inputTextArea">
                      <Form.Label>Enter a text sample.</Form.Label>
                      <Form.Control 
                        disabled={this.state.inputFile} 
                        onChange={() => this.handleText(this.textInput.value)} 
                        as="textarea" 
                        size="lg" 
                        rows="6" 
                        ref={text => {this.textInput = text}}
                      />
                      <br/>
                    </Form.Group>
                  </div>
                  <div className="divider"></div>
                  <div className="item Fileupload">
                    <Form.Group controlId="inputFileArea">
                      <Form.Label>Or choose a file to upload.</Form.Label>
                      <div className="custom-file">
                        <Form.Control 
                          type='file'
                          //controlId="customFile"
                          className="custom-file-input"
                          onChange={(event) => this.handleFile(event.target.files[0])} 
                          disabled={this.state.inputText}
                        />
                        <Form.Label className="custom-file-label Filelabel">
                          {this.state.inputFile ? this.fileName : "Choose File..."}
                        </Form.Label>
                      </div>
                      <br/>
                    </Form.Group>
                  </div>
                </div>
                <div className="nice-buttons">
                  <Button variant="primary" className="nice-button" type="submit" size='lg' disabled={!(this.state.inputText || this.state.inputFile)}>
                    Submit
                  </Button>
                  <Button variant="danger" className="nice-button" type="reset" size='lg' onClick={this.resetState}>
                    Clear
                  </Button>
                </div>
              </Form>
            </div>
          </div>
        </div>
      )

    } else {
      return (
        <div className="Submit">
          <header className="Submit-header">
            Thank you for submitting!
          <div style={{ width: 400 }}>
            <Loader type="Bars" color="#73a3ba" height={120} width={120} />
            <p>Sit tight. Your text is being processed!</p>
            <Button variant="danger" size="lg" onClick={this.resetState}>
              Cancel
            </Button> 
          </div>
          </header>
        </div>
      );
    }
  }
}

export default withRouter(App);
