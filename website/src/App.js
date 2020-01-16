import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Link } from 'react-router-dom'

import 'bootstrap/dist/css/bootstrap.min.css';

import {FormControl, Form, Button} from 'react-bootstrap';


import PersonList from './PersonList.js';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      text: '',
    }
    this.handleChange = this.handleChange.bind(this)
    this.sendTextToAPI = this.sendTextToAPI.bind(this)
  }

  componentDidMount() {
    console.log('Component Mounted')
  }

  handleChange(newText) {
    this.setState({
      text: newText,
    })
  }

  sendTextToAPI() {
    console.log('You should see input text below')
    const text = this.state.text
    console.log(text)

    // fetch('api/**SEND_ME_SOMEWHERE**', {
    //   method: 'POST',
    //   body: text,
    // })
  }

  render () {
    return (
      <div className="App">
        <div className="background">
          <div className="item">
          <header className="App-header">
              <Form onChange={() => this.handleChange(this.textInput.value)}>
              <Form.Group controlId="exampleForm.ControlTextarea1">
                  <Form.Label>Please enter a text sample!</Form.Label>
                  <Form.Control as="textarea" size="lg" rows="6" ref={text => {this.textInput = text}}/>
                  <Link to="/submit">
                  <Button variant="primary" type="submit" onClick={this.sendTextToAPI}>
                      Submit
                  </Button>
                  </Link>
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
    );
  }

}

export default App;
