
import React from 'react';
import './Submit.css';

import { Link } from 'react-router-dom'

import 'bootstrap/dist/css/bootstrap.min.css';

import { ProgressBar } from 'react-bootstrap';
import {FormControl, Form, Button} from 'react-bootstrap';


function Submit() {
  return (
    <div className="Submit">
      <header className="Submit-header">
        Thank you for submitting!
      <div style={{ width: 400 }}>
        <ProgressBar animated now={45} />
        <Form>
        <Form.Group controlId="exampleForm.ControlTextarea1">
            <Link to="/results">
            <Button variant="primary" type="submit">
                Go to results
            </Button>
            </Link>
        </Form.Group>
        </Form>
      </div>
      </header>
    </div>
  );
}

export default Submit;
