import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class StoryBoardQuiz extends React.Component {
  render() {
    return <div>

      <p> Storyboard Quiz Viewer </p>

      <button>Save </button><br />

      <Link to="/StoryBoardViewer">Back to Storyboard Viewer</Link>
        
    </div>
  }

}
