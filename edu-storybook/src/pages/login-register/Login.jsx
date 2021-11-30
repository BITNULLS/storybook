import React, {Component} from "react";
import { Link } from "react-router-dom";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import $ from 'jquery';

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

              <div class="form-group mb-4">
                <label for="email">E-mail:</label>
                <input id="email" type="text" formControlName="email" class="form-control"></input>
              </div>
              <div class="form-group mb-4">
                <OverlayTrigger
                  delay={{ hide: 450, show: 300 }}
                  overlay={(props) => (
                    <Tooltip class="pl-3 bg-info" {...props}>
                      <div align = 'left'>
                        <p>Must contain at least:</p>
                        <li>8 characters,</li>
                        <li>1 capital letter</li>
                        <li>1 special character (@$_*)</li>
                      </div>
                    </Tooltip>
                  )}
                  placement="top">
                  <a class="p-1 border-info">
                    <i class="bi bi-info-circle"></i>
                  </a>
                </OverlayTrigger>
                <label for="password">Password:</label>
                <input id= "password" type="password" formControlName="password" class="form-control"></input>
              </div>
              
              <form onSubmit={e => e.preventDefault()}>
              <div class="form-group">
                <Link to="/StorySelection">
                  <button id="button_signIn" class="btn btn-primary" onClick={() => sendLoginRequest()}>Sign In</button >
                </Link>
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

function sendLoginRequest() {
    let email = $('#email').val()
    let password = $('#password').val()

    $.ajax({
      type: "POST",
      url: "http://localhost:5000/login",
      contentType: "application/x-www-form-urlencoded",
      dataType: "json",
      data: {email, password},
      success: function(data){
        new Login(data)
        alert("Login Successful!")
      },
      error: function() {
        alert("Either email or password is incorrect. Please try again. ")
      }, 
  });
}
