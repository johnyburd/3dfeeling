import React from 'react'
import { withRouter } from 'react-router-dom'
import './Details.scss'

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
              <h1>About 3D Feeling</h1>
              <p>
                Our project, 3D Feeling, creates a 3D representation 
                of emotions found within a corpus of text. 
                This is not definitive, as extracting sentiment 
                from a text corpus and modeling it in 3D space 
                is an abstract problem that has no right answer. 
                Our solution generates 3D models that have a 
                quantitative and explainable foundation while 
                also instilling complex, indescribable emotion in the viewer. 
                We achieve this task by using information gathered 
                from natural language processing data collection 
                methods, which inspire a 3D model that can be 
                built in the real world.
              </p>
              <br />
              <p>
                This project was built by a team of six 
                Georgia Tech students for Dr. Krystin Gollihue. 
                Dr. Gollihue is a Marion L. Brittain Postdoctoral Fellow 
                at Georgia Tech, and the origin of this wonderful idea.
              </p>
              <br />
              <p>
                Our logo is inspired by an emotion 
                classification model known as plutchick's 
                wheel. <u><a href="https://en.wikipedia.org/wiki/Robert_Plutchik">See where it comes from</a></u>.
              </p>
              <br />
              <p>
                VAD Explanation: The website uses an NLP model that predicts 
                the Valence, Arousal, and Dominance (VAD) in each sentence 
                and uses those values to generate a unique 3D object that 
                represents those values. You can read more about this method of emotion 
                classification <u><a href="https://en.wikipedia.org/wiki/Emotion_classification">here</a></u>.
              </p>
              <br />
              <p>
                Classifier Methodology: The current NLP model uses 
                a <u><a href="https://en.wikipedia.org/wiki/Bag-of-words_model">bag-of-words</a></u> model 
                to capture the text in each sentence. This bag of words 
                is then fed into a naïve bayes which will output the VAD 
                levels of each sentence.
              </p>
              <br />
              <p>
                Object Generation: The first method of object generation 
                was to simply create a 3D histogram of the VAD level in 
                each sentence. This was used as a proof of concept model 
                generation technique and as a stepping stone to more 
                complicated techniques. The current object generation 
                algorithm that you can see now generates a terrain 
                where each ridge represents 
                the emotion in each sentence. A custom formula 
                takes into account the VAD variables to generate a curve 
                that represents the emotion in that sentence. Many points 
                are then sampled from this curve which are put into the 
                object. These are then all connected together to generate 
                a terrain that represents the entirety of emotion in the text.
              </p>
              <br />
              <p>
                Stuff for Nerds: Tools and technologies. 
                Check out <u><a href="https://github.com/johnyburd/3dfeeling">our repository</a></u>!
              </p>
              <br />
              <p>(Put rights and licensing here)</p>
            </div>
          </div>
        </div>
    )
  }
}

export default withRouter(Details);
