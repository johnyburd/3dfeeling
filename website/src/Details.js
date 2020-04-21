import React from 'react'
import { withRouter } from 'react-router-dom'
import './Details.scss'
import logo from './3dfeeling_logo.png'

import 'bootstrap/dist/css/bootstrap.min.css'

import Feelbar from './Feelbar'

class Details extends React.Component {

  componentDidMount() {
    console.log('Details Mounted')
  }

  render () {
    return (
        <div className="Details">
          <Feelbar />
          <div className="Details-header">
            <div className="Details-content">
              <h1 className="title">About 3D Feeling <img alt="3D Feeling Logo" width="36px" height="36px" src={logo}></img></h1>
              <p>
                Our project, 3D Feeling, creates a 3D representation
                of emotions found within a corpus of text.
              </p>
              <p>
                The results you see from this project are not definitive,
                nor do they claim to be perfect representations of emotion.
                Having built this unique service, we certainly know that
                extracting sentiment from a text corpus and modeling it in 3D space
                is an abstract problem that has no right or wrong answer.
                However, this is one interesting answer to a task
                no one has attempted before to our knowledge.
                This project generates 3D models that have a
                quantitative and explainable foundation, while
                also instilling complex, indescribable emotion in the viewer.
              </p>
              <p>
                We achieve this task by using information gathered
                from natural language processing data collection
                methods, which inspire a 3D model that can be
                built in the real world.
              </p>
              <br />

              <h4 className='Sub-header'>Who built this?</h4>
              <p>
                This project was built by a team of six
                Georgia Tech students for Dr. Krystin Gollihue.
                Dr. Gollihue is a Marion L. Brittain Postdoctoral Fellow
                at Georgia Tech, and the origin of this wonderful idea.
              </p>
              <br />

              <h4 className='Sub-header'>Nice logo. Where'd you get it?</h4>
              <p>
                Our logo is inspired by an emotion
                classification model known as plutchick's
                wheel. <a href="https://en.wikipedia.org/wiki/Robert_Plutchik">Click
                here to see where it comes from</a>.
              </p>
              <br />

              <h4 className='Sub-header'>VAD Explanation</h4>
              <p>
                The website uses an NLP (Natural Language Processing) model that predicts
                the Valence, Arousal, and Dominance (VAD) in each sentence
                and uses those values to generate a unique 3D object that
                represents those values. If you're curious about what VAD values are,
                You can read more about this method of emotion
                classification <a href="https://en.wikipedia.org/wiki/Emotion_classification">here</a>.
              </p>
              <br />

              <h4 className='Sub-header'>Classifier Methodology</h4>
              <p>
                The previous NLP model used
                a <a href="https://en.wikipedia.org/wiki/Bag-of-words_model">bag-of-words</a> model
                to capture the text in each sentence. This bag of words
                was then fed into a naïve bayes which output the VAD
                levels of each sentence.
              </p>
              <p>
                The current NLP model uses 25 dimensional Glove
                embeddings trained on twitter data. The features
                are classified using three <a href='https://en.wikipedia.org/wiki/Long_short-term_memory'>LSTM</a> (Long
                Short-Term Memory) models that
                predict the VAD values for each sentence.
              </p>
              <br />
              <h4 className='Sub-header'>Object Generation</h4>
              <p>
                The first method of object generation
                was to simply create a 3D histogram of the VAD level in
                each sentence. This was used as a proof of concept model
                generation technique and as a stepping stone to more
                complicated techniques.
              </p>
              <p>
                The next object generation
                algorithm generated a terrain
                where each ridge represents
                the emotion in each sentence. A custom formula
                takes into account the VAD variables to generate a curve
                that represents the emotion in that sentence. Many points
                are then sampled from this curve which are put into the
                object. These are then all connected together to generate
                a terrain that represents the entirety of emotion in the text.
                </p>
                <p>
                The current object generation is similar to the previous one
                but the VAD formula is wrapped around a polygon and the 
                polygons are stacked cylindrically. For every group of 10
                sentences, the dominance value furthest from 0.5 is taken
                and used to generate a regular polygon with some number of 
                sides. The higher the dominance the closer the polygon will 
                be to a triangle and the lower it is the closer it will be to 
                an octagon. The values from the VAD function are added to the 
                points on the polygon to give it a rougher edge reresenting 
                the full spectrum of valence, arousal, and dominance from each
                sentence. All of these polygons are then stacked together and 
                connected up to create the final shape.
              </p>
              <br />

              <h4 className='Sub-header'>Stuff for Nerds</h4>
              <p>
                This website is built using React and styled with React bootstrap components.
              </p>
              <p>
                Requests are made using axios to our server, which allows for multiple requests
                by utilizing queueing and parallel processing.
              </p>
              <p>
                Those parallel processes run our Natural Language Processing and Object Generation
                algorithms, which you can read about above if you haven't already.
              </p>
              <p>
                After those are finished, the VAD values generated from sentiment analysis and the STL
                file are sent back, along with visuals and other goodies like a color recommendation
                for the user to see on the results page.
              </p>
              <br />
              <br />
              <h4 className='Sub-header'>Licensing and our Code</h4>
              <p>
                Created with an MIT License. Please read this thoroughly if you
                wish to modify/add to this project and make it your own in any way.
              </p>
              <p className='subtle'>
                Permission is hereby granted, free of charge, to any person obtaining a copy
                of this software and associated documentation files (the "Software"), to deal
                in the Software without restriction, including without limitation the rights
                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is
                furnished to do so, subject to the following conditions:

                The below copyright notice and this permission notice shall be included in all
                copies or substantial portions of the Software.

                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                SOFTWARE.
              </p>
              <p>
                So if you're into programming like we are,
                check out <u><a href="https://github.com/johnyburd/3dfeeling">our repository</a></u>!
              </p>
              <p>
                Copyright © 2020 <strong>Team 3D Feeling <img alt="3D Feeling Logo" width="12px" height="12px" src={logo}></img> JIC 9328</strong>
              </p>
            </div>
          </div>
        </div>
    )
  }
}

export default withRouter(Details);
