import React, {useState} from "react";
import { NavLink } from "react-router-dom";

/**
 * 
 * @returns 
 */
const ResetPassword = (props) => {
  return(
    <div>

      <p> Reset Password </p>

      <input placeholder="New Password" type="password" /><br />
      <input placeholder="Confirm Password" type="password" /><br /><br />
          
      <NavLink exact activeClassName="active" to="/Login">Confirm </NavLink><br />

    </div>
  )

}

export default ResetPassword;
