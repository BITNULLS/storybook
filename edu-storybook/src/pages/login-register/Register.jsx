import React from "react";
import { Link } from "react-router-dom";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import $ from 'jquery';

export default class Register extends React.Component {
  render() {
    return (
      <div class="row mt-5">
        <div class="col-12 col-md-4 col-sm-3"></div>
        <div class="col">
          <h1 class="text-center mb-5">Register</h1>

          <div class="card pl-1 pr-2">
            <div class="card-body">
              <form>

                <div class="row">
                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="first_name">First Name:</label>
                      <input id="first_name" type="text" formControlName="first_name" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="last_name">Last Name:</label>
                      <input id="last_name" type="last_name" formControlName="last_name" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="email">Email Address:</label>
                      <input id="email" type="text" formControlName="email" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="school_id">School ID:</label>
                      <input id="school_id" type="text" formControlName="school_id" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-12 col-sm-6">
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
                      <input id="password" type="text" formControlName="password" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
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
                      <label for="confirm_password">Confirm Password:</label>
                      <input id="confirm_password" stype="text" formControlName="confirm_password" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <form onSubmit={e => e.preventDefault()}>
                  <div class="form-group">
                    <Link to="/Register">
                      <button id="button_signUp" class="btn btn-primary" onClick={
                        function sendRegisterRequest() {
                          
                          let first_name = $('#first_name').val()
                          let last_name = $('#last_name').val()
                          let email = $('#email').val()
                          let school_id = $('#school_id').val()
                          let password = $('#password').val()
                          let confirm_password = $('#confirm_password').val()
                
                          if (password=confirm_password)
                            $.ajax({
                              type: "POST",
                              url: "http://localhost:5000/register",
                              contentType: "application/x-www-form-urlencoded",
                              dataType: "json",
                              data: {first_name, last_name, school_id, email, password},
                              success: function(data){
                                new Register(data)
                                alert("Register Successful!" )
                              },
                              error: function() {
                                alert("Something went wrong with your registration. Please try again. ")
                              }, 
                            });
                          else 
                          alert("Passwords do not match. Please try again.")
                        }
                      }>Sign In</button >
                    </Link>
                  </div>
                </form>

              </form>
            </div >
          </div>

          <div class="text-center mt-5">
            <Link to="/Login" class="btn btn-link">Login</Link>
            <Link to="/ForgotPassword" class="btn btn-link">Forgot Password</Link>
          </div>
        </div >
        <div class="col col-12 col-md-4 col-sm-3"></div>
      </div >
    );
  }
}