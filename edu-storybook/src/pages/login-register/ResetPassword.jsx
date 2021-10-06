import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class ResetPassword extends React.Component {
  render() {
    return <div>

      <p> Reset Password </p>

      <input placeholder="New Password" type="password" /><br />
      <input placeholder="Confirm Password" type="password" /><br /><br />

      <Link to="/Login">Confirm </Link>

    </div>;
  }

}
