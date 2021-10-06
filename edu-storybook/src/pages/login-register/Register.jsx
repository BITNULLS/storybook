import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class Register extends React.Component {

  render() {
    return <div>

      <p> Register </p>

      <input placeholder="First Name" type="text" /><br />
      <input placeholder="Last Name" type="text" /><br /><br />
        
      <input placeholder="Username" type="text" /><br />
      <input placeholder="Password" type="password" /><br /><br />        
      <input placeholder="Email" type="text" /><br />
      <input placeholder="Confirm Password" type="password" /><br /><br />
          
      <button>Submit</button>
          
    </div>;
  }

}
