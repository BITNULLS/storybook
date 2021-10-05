import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const HomePage = (props) => {

  return(
    <div className="HomePage">

      <p> Home Page </p>

      <button onClick={() => 
        props.history.push('/Login')
      }>Login </button>

      <button onClick={() => 
        props.history.push('/Register')
      }>Register </button>

    </div> 
  )

}

export default HomePage;