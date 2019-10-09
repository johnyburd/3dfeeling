import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Enter some text to get a nice 3d model :)
        </p>
	  <form>
	    <label>
	      Text:
	      <input type="text" name="Text" />
	    </label>
	    <input type="submit" value="Submit" />
	  </form>
      </header>
    </div>
  );
}

export default App;
