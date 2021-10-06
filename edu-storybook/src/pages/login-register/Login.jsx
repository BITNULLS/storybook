import React, {Component} from "react";
import { NavLink } from "react-router-dom";
import { Link } from "react-router-dom";

/** This is the Login Page
 *  This is an example of a class for React
 */
export default class Login extends React.Component {
  render() {
    return <div>

      <p> Login </p>

      <input placeholder="Username" type="text" /><br />
      <input placeholder="Password" type="password" /><br /><br />
            
      <Link to="/Register">Register</Link><br />
      <Link to="/ForgotPassword">Forgot Password</Link><br /><br />

      <Link to="/StorySelection">Sign in</Link>  

      <Link to="/AdminSignIn">Admin Sign In</Link>
          
    </div>
  };
  
}
