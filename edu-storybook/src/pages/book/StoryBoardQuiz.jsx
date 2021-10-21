import React from "react";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
import { Col } from "react-bootstrap";
import { Container } from "react-bootstrap";
import ButtonGroup from 'react-bootstrap/ButtonGroup'

/**
 * 
 * @returns 
 */
export default class StoryBoardQuiz extends React.Component {
  render() {
    return <div>
      
      <h1> Check for Understanding </h1>
      <div class= "row mt-5"> </div>

      <h4> Marta is taking a science test about the ecosystems in her state. <br/> Which of the following is most likely to
      influence her self-efficacy for this test? </h4>
    
      <div class= "row mt-5"> </div>  
        <div class="container">
          <div class="row">
        
            <div class="col p-4">
              <Button variant="primary" type="submit" class="mcBtn">How well she did on her math test yesterday. </Button>{' '}
         </div>
    
            <div class="col p-4"> 
              <Button variant="primary" type="submit" class="mcBtn">Her enjoyment of the field trip to the seashore
              <br/> to study the ecosystem there. </Button>{' '} 
          </div>

          <div class="w-100"></div>
          
          <div class="col mb-auto p-4">
            <Button variant="primary" type="submit" class="mcBtn">Her teacher’s compliment of her answer to a question <br/> 
            on the seashore field trip. </Button>{' '} 
          </div>
        
        <div class="col flex-md-first mb-auto p-4">
        <Button variant="primary" type="submit" class="mcBtn">Her dream of one day being a Chemist. </Button>{' '}
        </div>
      
      </div>
  </div>
        
        <Link to="/StoryBoardViewer">Back to Storyboard Viewer</Link>         
    </div>
  }
}

