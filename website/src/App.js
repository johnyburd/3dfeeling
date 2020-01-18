import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Link } from 'react-router-dom'

import 'bootstrap/dist/css/bootstrap.min.css';

import {FormControl, Form, Button} from 'react-bootstrap';


import GuildCount from './GuildCount.js';

function App() {
  return (
    <div className="App">
      <div className="background">
        <div className="item">
        <header className="App-header">
          <GuildCount/>
          <Form>
          <Form.Group controlId="exampleForm.ControlTextarea1">
            <Form.Label>Please enter a text sample!</Form.Label>
            <Form.Control as="textarea" size="lg" rows="6" />
            <Link to="/submit">
            <Button variant="primary" type="submit">
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

export default App;
