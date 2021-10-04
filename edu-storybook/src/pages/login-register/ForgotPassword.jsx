import React, {useState} from "react";
import ResetPassword from "./ResetPassword";
/**
 * 
 * @returns 
 */
function ForgotPassword(){

  return(
      <div>

          <input placeholder="Username" type="text" /><br />
          <input placeholder="Email" type="text" /><br /><br />
          <button>Send Email</button>
          
      </div>
  )

}

export default ForgotPassword;
