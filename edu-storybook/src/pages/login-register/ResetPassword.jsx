import React, {Component} from "react";
import ReactTooltip from 'react-tooltip';
import IconButton from "@material-ui/core/IconButton";
import Info from "@material-ui/icons/Info";

/**
 * 
 * Creates a new password if valid credentials are found from ForgotPassword page
 * Add backend: updates the old password stored in database
 * 
 */
export default class ResetPassword extends React.Component{
 render() {
    return (
      <div class="row mt-5">
        <div class="col"></div>
        <div class="col">
          <h1 class="text-center mb-5"> Reset Password </h1>  
              <form>
                <div class="form-group mb-4">
                  <label for="username">New Password:</label>
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
                  <input type="text" formControlName="username" class="form-control"></input>
                </div>
                <div class="form-group mb-4">
                  <label for="password">Confirm Password:</label>
                  <input type="password" formControlName="password" class="form-control"></input>
                  <p class="mb-5"> Password must be at least eight characters </p>  
                </div>
                <div class="text-center form-group">
                  <button class="btn btn-primary">Confirm</button >
                </div>
              </form>

          <div class="text-center mt-5">
          </div>
        </div >
        <div class="col"></div>
      </div >
    );
  }
}
