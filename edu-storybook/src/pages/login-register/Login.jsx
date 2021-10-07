import React, {Component} from "react";
import { NavLink } from "react-router-dom";
import { Link } from "react-router-dom";

/** This is the Login Page
 *  This is an example of a class for React
 */
export default class Login extends React.Component {
  render() {
    return(
      <div class="row mt-5">
      <div class="col-12 col-md-4 col-sm-3"></div>
      <div class="col">
        <h1 class="text-center mb-5">Login</h1>

        <div class="card pl-1 pr-2">
          <div class="card-body">
            <form>

              <div class="form-group mb-4">
                <label for="username">Username:</label>
                <input type="text" formControlName="username" class="form-control"></input>
              </div>

              <div class="form-group mb-4">
                <label for="password">Password:</label>
                <input type="password" formControlName="password" class="form-control"></input>
              </div>

              <div class="form-group">
                <button class="btn btn-primary">Sign In</button >
              </div>

            </form>

          </div >

        </div>

        <div class="text-center mt-5">
          <Link to="/Register" class="btn btn-link">Register</Link>
          <Link to="/ForgotPassword" class="btn btn-link">Forgot Password</Link>
        </div>
      </div >
      <div class="col-12 col-md-4 col-sm-3"></div>
    </div >
    );
    
  }
}
