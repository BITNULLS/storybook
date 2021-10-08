import React, {Component} from "react";
import { Link } from "react-router-dom";

/**
 * 
 * Displays the 'username' and 'email address' fields with 'send email' button
 * Add backend: searches for a matching username (hit/miss) first and then sends email
 * Add: if invalid username/email, error message display
 *
 */
export default class ForgotPassword extends React.Component {

  render() {
    return (
      <div class="row mt-5">
        <div class="col"></div>
        <div class="col">
          <h1 class="text-center mb-5">Forgot Your Password? </h1>
          <h4 class="text-center mb-5"> Don't worry! We will send you an email to update your password. </h4>
  
              <form>
                <div class="form-group mb-4">
                  <label for="username">Username:</label>
                  <input type="text" formControlName="username" class="form-control"></input>
                </div>
                <div class="form-group mb-4">
                  <label for="password">Email Address:</label>
                  <input type="password" formControlName="password" class="form-control"></input>
                </div>
                <div class="text-center form-group">
                  <button class="btn btn-primary">Send Email</button >
                </div>
              </form>

          <div class="text-center mt-5">
            <Link to="/Login" class="btn btn-link">Back to Sign In</Link>
          </div>
        </div >
        <div class="col"></div>
      </div >
    );
  }
}