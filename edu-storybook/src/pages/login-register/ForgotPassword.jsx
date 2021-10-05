import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const ForgotPassword = (props) => {
  return(
    <div>

      <p> Forgot Password </p>

      <input placeholder="Username" type="text" /><br />
      <input placeholder="Email" type="text" /><br /><br />
      <button>Send Email</button>
          
    </div>
  )

}

export default ForgotPassword;
