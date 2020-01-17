import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Submit from './Submit';
import Results from './Results';

import { Route, Link, BrowserRouter as Router } from 'react-router-dom'

import * as serviceWorker from './serviceWorker';


const routing = (
  <Router>
    <div>
      <Route exact path="/" component={App} />
      <Route path="/submit" component={Submit} />
      <Route path="/results" component={Results} />
    </div>
  </Router>
)
ReactDOM.render(routing, document.getElementById('root'))


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
