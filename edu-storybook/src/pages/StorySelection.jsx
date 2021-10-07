import React from "react";
import { Link } from "react-router-dom";

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

export default class StorySelection extends React.Component {
  render() {
    return <div>
    
      <div>
        {/*Navigation Bar Here*/}
        <h1>Story Selection</h1>
        <h2>Choose a Story to Read:</h2>
        <div>{/*Buffer Space*/}</div>
        {/*Add Books Here*/}
      </div>

    </div>;
  }

}
