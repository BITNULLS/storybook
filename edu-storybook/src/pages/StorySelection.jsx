import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const StorySelection = (props) => {
  return(
    <div>
      
      <p> Story Selection </p>

      <button onClick={() => 
        props.history.push('/StoryBoardViewer')
      }>Read Now! </button>  

    </div>
  )

}

export default StorySelection;
