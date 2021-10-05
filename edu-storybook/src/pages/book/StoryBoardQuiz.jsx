import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const StoryBoardQuiz = (props) => {
  return(
    <div>

      <p> Storyboard Quiz Viewer </p>

      <button>Save </button><br />

      <button onClick={() => 
        props.history.push('/StoryBoardViewer')
      }>Back to Storyboard Viewer </button> 
        
    </div>
  )

}

export default StoryBoardQuiz;
