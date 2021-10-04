import React, {useState} from "react";
import HomePage from "../HomePage"
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function ResetPassword(){

  return(
    <Router>
      <div>

          <input placeholder="New Password" type="password" /><br />
          <input placeholder="Confirm Password" type="password" /><br /><br />
          
          <Link to="/HomePage">
            <button>Confirm</button>
          </Link> 

          <Switch> 
            <Route path="/HomePage" component={HomePage} />
          </Switch>

      </div>
    </Router>
  )

}

export default ResetPassword;
