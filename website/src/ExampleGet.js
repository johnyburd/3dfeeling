import React, { useState, useEffect } from 'react';
import axios from 'axios';


export default function ExampleGet() {
  const [data, setData] = useState([]);
  useEffect(() => {
    axios.get(`https://api.3dfeeling.ga/example`)
      .then(res => {
        //const data = res.data;
        setData(res.data);
      })
  }, []);
  return (
    <ul>
      <li>
        Valence: { data.valence }%
      </li>
      <li>
        Arousal: { data.arousal }%
      </li>
      <li>
        Dominance: { data.dominance }%
      </li>
    </ul>
  );
}
