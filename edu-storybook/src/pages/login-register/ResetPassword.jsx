import React, {Component} from "react";

/**
 * 
 * Creates a new password if valid credentials are found from ForgotPassword page
 * Add backend: updates the old password stored in database
 * 
 */

 class  ResetPassword extends React.Component{

 render() {
    return (
      <div class="row mt-5">
        <div class="col"></div>
        <div class="col">
          <h1 class="text-center mb-5"> Reset Password </h1>  
              <form>
                <div class="form-group mb-4">
                  <label for="username">New Password:</label>
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
export default ResetPassword;