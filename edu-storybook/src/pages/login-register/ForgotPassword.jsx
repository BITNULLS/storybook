import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class ForgotPassword extends React.Component {
  render() {
    return <div>

      <p> Forgot Password </p>

      <input placeholder="Username" type="text" /><br />
      <input placeholder="Email" type="text" /><br /><br />
      <button>Send Email</button>
          
    </div>;
  }

}
