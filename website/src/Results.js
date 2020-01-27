import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Results.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import STLViewer from 'stl-viewer';

// Test model? 'https://bohdanbirdie.github.io/stl-obj-demo/bottle.stl'

function Results() {
  const [valence, setValence] = useState()
  const [arousal, setArousal] = useState()
  const [dominance, setDominance] = useState()
  const [inputText, setInputText] = useState()
  useEffect(() => {
    axios.get(`https://api.3dfeeling.ga/example`)
      .then(res => {
        //const data = res.data;
        // setData(res.data);
        setValence(res.data.valence)
        setArousal(res.data.arousal)
        setDominance(res.data.dominance)
      })
  }, []);

  return (
    <div className="Results">
      <div className="Background">
        <div className='item'>
          <div className='Results-header'>
            Results and shape will be displayed here
            <STLViewer
              model={'https://api.3dfeeling.ga/assets/b82be92e-5fa3-4040-bf24-0afb4ec0da39.stl'}
              width={400}
              height={400}
              modelColor='#EAEAEA'
              backgroundColor='#222222'
              rotate={true}
              orbitControls={true}
            />
          <p>Input text: {inputText}</p>
          <ul>
            <li>
              Valence: { valence }%
            </li>
            <li>
              Arousal: { arousal }%
            </li>
            <li>
              Dominance: { dominance }%
            </li>
          </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Results;
