
import React from 'react';
import './Submit.css';

import 'bootstrap/dist/css/bootstrap.min.css';

import { ProgressBar } from 'react-bootstrap';



function App() {
  return (
    <div className="App">
      <header className="App-header">
        Thank you for submitting!
      <div style={{ width: 400 }}>
        <ProgressBar animated now={45} />
      </div>
      </header>
    </div>
  );
}

export default App;
