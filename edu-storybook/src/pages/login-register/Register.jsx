import React from "react";
import { Link } from "react-router-dom";
import ReactTooltip from 'react-tooltip';
import IconButton from "@material-ui/core/IconButton";
import Info from "@material-ui/icons/Info";


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
                      <label for="username">Username:</label>
                      <input type="text" formControlName="username" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="email">Email Address:</label>
                      <input type="email" formControlName="email" class="form-control"></input>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="password">Password:</label>
                      <a data-tip data-for='info'> 
                        <IconButton>
                          <Info />
                        </IconButton> 
                      </a>
                      <ReactTooltip id='info' aria-haspopup='true' >
                      <div align = 'left'>
                        <p>Password must contain at least:</p>
                        <li>8 characters,</li>
                        <li>one capital letter</li>
                        <li>one special character ( @$*_ )</li>
                      </div>
                      </ReactTooltip>
                      <input type="text" formControlName="password" class="form-control"></input>
                    </div>
                  </div>

                  <div class="col-12 col-sm-6">
                    <div class="form-group mb-4">
                      <label for="conf_pass">Confirm Password:</label>
                      <a data-tip data-for='info-confirm'> 
                        <IconButton>
                          <Info />
                        </IconButton> 
                      </a>
                      <ReactTooltip id='info-confirm' aria-haspopup='true' >
                      <div align = 'left'>
                        <p>Password must contain at least:</p>
                        <li>8 characters,</li>
                        <li>one capital letter</li>
                        <li>one special character ( @$*_ )</li>
                      </div>
                      </ReactTooltip>
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