import React, {useState} from "react";

/**
 * 
 * @returns 
 */

function Book(props) {
  return(
    <div>
      <div>
        {props.title}
      </div>
      <div>
        <img src={props.image}></img>
      </div>
      <div>
        {props.description}
      </div>
    </div>
  )
}

export default function StorySelection(){

  return(
    <div>
      {/*Navigation Bar Here*/}
      <h1>Story Selection</h1>
      <h2>Choose a Story to Read:</h2>
      <div>{/*Buffer Space*/}</div>
      {/*Add Books Here*/}
    </div>
  )

}