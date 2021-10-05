import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const EditBook = (props) => {
  return(
    <div>

      <p> Edit Quizzes </p>

      <button onClick={() => 
        props.history.push('/AdminViewPage')
      }>Back </button>

      <button>Save </button>
      <button>Publish </button>

      </div>
  )

}

export default EditBook;
