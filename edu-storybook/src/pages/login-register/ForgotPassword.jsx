import React, { Component } from "react";
import { Link } from "react-router-dom";
import $ from 'jquery';

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
        <div class="col-12 col-md-4 col-sm-3"></div>
        <div class="col">
          <h1 class="text-center mb-5">Forgot Your Password? </h1>
          <h4 class="text-center mb-5"> Don't worry! We will send you an email to update your password. </h4>

          <form>
            <div class="form-group mb-4">
              <label for="email">Email Address:</label>
              <input id="email" type="email" formControlName="email" class="form-control"></input>
            </div>
            <div class="text-center form-group">
              <button id="submit-button" class="btn btn-primary" onClick={

                function sendEmailAddress() {
                  let email = $("#email").val();
                  console.log(email);

                  $.ajax({
                    type: "POST",
                    url: "/password/forgot",
                    contentType: "application/x-www-form-urlencoded",
                    dataType: "json",
                    async: false,
                    data: { email },

                    success: function (data) {
                      alert("Forgot Password Successful!")
                      new ForgotPassword(data)
                      this.iat = data["iat"]
                    },

                    error: function () {
                      alert("Email is incorrect. Please try again.")
                    },
                  });
                }
              } >Send Email</button >
            </div>
          </form>

          <div class="text-center mt-5">
            <Link to="/Login" class="btn btn-link">Back to Sign In</Link>
          </div>
        </div >
        <div class="col-12 col-md-4 col-sm-3"></div>
      </div >
    );
  }
}
