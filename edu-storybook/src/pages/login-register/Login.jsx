import React, {Component} from "react";
import { NavLink } from "react-router-dom";

/** This is the Login Page
 *  This is an example of a class for React
 */
const Login = (props) => {
  return(
    <div>

      <p> Login </p>

      <input placeholder="Username" type="text" /><br />
      <input placeholder="Password" type="password" /><br /><br />
            
      <NavLink exact activeClassName="active" to="/Register">Register </NavLink><br />
      <NavLink exact activeClassName="active" to="/ForgotPassword">Forgot Password </NavLink><br /><br />

      <button onClick={() => 
        props.history.push('/StorySelection')
      }>Sign In </button>   

      <button onClick={() => 
        props.history.push('/AdminSignIn')
      }>Admin Sign In </button>      
          
    </div>
  )
  
}

export default Login;
