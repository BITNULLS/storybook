import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class StoryBoardViewer extends React.Component {
  render() {
    return <div>

      <p> Storyboard Viewer </p>

      <Link to="/StoryBoardQuiz">Go to Quiz</Link>
      <Link to="/StorySelection">Back to Story Selection</Link>
    
    </div>;
  }

}
