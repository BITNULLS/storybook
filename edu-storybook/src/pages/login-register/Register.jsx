import React from "react";
import { Link } from "react-router-dom";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';

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
                      <input type="text" formControlName="first_name" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="last_name">Last Name:</label>
                      <input type="last_name" formControlName="last_name" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="username">Email Address:</label>
                      <input type="text" formControlName="username" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="email">Take Part Study:</label>
                      <input type="email" formControlName="email" class="form-control"></input>
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
                      <input type="text" formControlName="password" class="form-control"></input>
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
                      <label for="conf_pass">Confirm Password:</label>
                      <input type="conf_pass" formControlName="conf_pass" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <button class="btn btn-primary">Sign Up</button >
                </div>

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