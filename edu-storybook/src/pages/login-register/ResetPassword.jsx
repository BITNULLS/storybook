import React, {Component} from "react";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';

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
        <div class="col-12 col-md-4 col-sm-3"></div>
        <div class="col">
          <h1 class="text-center mb-5"> Reset Password </h1>  
              <form>
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
                  <label for="new_pass">New Password:</label>
                  <input type="text" formControlName="new_pass" class="form-control"></input>
              {/* TODO: take reset_key from url, like "url.com/.../reset#key=A93CDG043..." and automatically populate the reset_key field */}
                  <label for="reset_key"> </label>
                  <input type="text" formControlName="reset_key" class="form-control"></input>

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
                  <label for="confirm_pass">Confirm Password:</label>
                  <input type="password" formControlName="confirm_pass" class="form-control"></input> 
                </div>
                <div class="text-center form-group">
                  <button class="btn btn-primary">Confirm</button >
                </div>
              </form>

          <div class="text-center mt-5">
          </div>
        </div >
        <div class="col-12 col-md-4 col-sm-3"></div>
      </div >
    );
  }
}
