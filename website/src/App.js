import React from 'react'
import logo from './logo.svg'
import './App.css';

import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';

import { ProgressBar } from 'react-bootstrap';
import {Form, Button} from 'react-bootstrap';
import STLViewer from 'stl-viewer';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      inputText: '',
      loading: false,
      loaded: false,
      valence: '',
      arousal: '',
      dominance: '',
      fileName: '',
    }
    this.handleChange = this.handleChange.bind(this)
    this.sendTextToAPI = this.sendTextToAPI.bind(this)
    this.pointsAverage = this.pointsAverage.bind(this)
  }

  componentDidMount() {
    console.log('Component Mounted')
  }

  handleChange(newText) {
    this.setState({
      inputText: newText,
    })
  }

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

  sendTextToAPI(event) {
    let currentComponent = this
    let retrievedData = {
      fileName: "Didnt work", 
      points: [[-1, -1, -1]],
    }
    event.preventDefault()
    console.log('You should see input text below')
    const text = this.state.inputText
    console.log(text)
    this.setState({
      loading: true
    })
    axios.post('https://api.3dfeeling.ga/analyze',
      `text=${this.state.inputText}`
    ).then(function (resp) {
      //Assign gathered sentiment analysis values here
      console.log(resp)
      retrievedData = resp.data
      let averages = currentComponent.pointsAverage(retrievedData.points)
      currentComponent.setState({
        loading: false,
        loaded: true,
        valence: averages[0],
        arousal: averages[1],
        dominance: averages[2],
        fileName: retrievedData.filename
      })
      console.log(retrievedData);
    }).catch(function (error) {
      console.log(error);
    });
  }

  render () {
    if (!this.state.loading && !this.state.loaded) {
      return (
        <div className="App">
          <div className="background">
            <div className="item">
              <header className="App-header">
                <Form onChange={() => this.handleChange(this.textInput.value)}>
                <Form.Group controlId="exampleForm.ControlTextarea1">
                  <Form.Label>Please enter a text sample!</Form.Label>
                  <Form.Control as="textarea" size="lg" rows="6" ref={text => {this.textInput = text}}/>
                  <Button variant="primary" type="submit" onClick={this.sendTextToAPI}>
                    Submit
                  </Button>
                </Form.Group>
                </Form>
              </header>
            </div>
            <div className="divider" />
            <div className="item">
              <p>Or choose a file to upload</p>
              <input type="file"/>
            </div>
          </div>
        </div>
      )
    } else if (this.state.loading && !this.state.loaded) {
      return (
        <div className="Submit">
          <header className="Submit-header">
            Thank you for submitting!
          <div style={{ width: 400 }}>
            <ProgressBar animated now={45} />
            <p>Sit tight. Your text is being processed!</p>
            <p>(Please do not refresh the page)</p>
          </div>
          </header>
        </div>
      );
    } else if (!this.state.loading && this.state.loaded) {
      return (
        <div className="Results">
          <div className="Background">
            <div className='item'>
              <div className='Results-header'>
                <h2>This is your shape in all of its glory!</h2>
                <p>Analysis values and the text it was generated from are below.</p>
                <STLViewer
                  model={'https://api.3dfeeling.ga/assets/' + this.state.fileName}
                  //model={'https://api.3dfeeling.ga/assets/b82be92e-5fa3-4040-bf24-0afb4ec0da39.stl'}
                  width={400}
                  height={400}
                  modelColor='#EAEAEA'
                  backgroundColor='#222222'
                  rotate={true}
                  orbitControls={true}
                />
              <ul>
                <li>
                  Valence: { this.state.valence }
                </li>
                <li>
                  Arousal: { this.state.arousal }
                </li>
                <li>
                  Dominance: { this.state.dominance }
                </li>
              </ul>
              <p>Input text: {this.state.inputText}</p>
              </div>
            </div>
          </div>
        </div>
      )
    }
    
  }

}

export default App;
