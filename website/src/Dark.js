import React from 'react';
import useDarkMode from 'use-dark-mode';

import './Dark.scss'


const DarkModeToggle = () => {
  const darkMode = useDarkMode(false);

  return (
    <div>
      <button type="button" className="btn btn-outline-info darkButton" onClick={darkMode.toggle}>
        ☾
      </button>
    </div>
  );
};

export default DarkModeToggle;