import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const StoryBoardViewer = (props) => {
  return(
    <div>

      <p> Storyboard Viewer </p>

      <button onClick={() => 
        props.history.push('/StoryBoardQuiz')
      }>Go to Quiz </button><br />

      <button onClick={() => 
        props.history.push('/StorySelection')
      }>Back to Story Selection </button>    
    
    </div>
  )

}

export default StoryBoardViewer;
