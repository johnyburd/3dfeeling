import React from 'react';
import useDarkMode from 'use-dark-mode';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'

import './Dark.scss'


const DarkModeToggle = () => {
  const darkMode = useDarkMode(false);

  return (
    <div>
      <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />

      <button type="button" className="btn btn-outline-info darkButton" onClick={darkMode.toggle}>
          <FontAwesomeIcon icon={faMoon} hidden={darkMode.value} />
          <FontAwesomeIcon icon={faSun} hidden={!darkMode.value} />
      </button>
    </div>
  );
};

export default DarkModeToggle;