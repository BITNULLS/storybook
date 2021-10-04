import React, {Component} from "react";
import Register from "./Register";
import ForgotPassword from "./ForgotPassword";
import StorySelection from "../../pages/StorySelection"
import AdminViewPage from "../../pages/admin/AdminViewPage"
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/** This is the Login Page
 *  This is an example of a class for React
 */
class Login extends React.Component {
  render() {
    return(
      <Router>
        <div>

          <p> Login </p>

          <input placeholder="Username" type="text" /><br />
          <input placeholder="Password" type="password" /><br /><br />
            
          <Link to="/Register">Register</Link> <br />
          <Link to="/ForgotPassword">Forgot Password</Link> <br /><br />
          <Link to="/SignIn">
            <button>Sign In</button>
            </Link> 
          <Link to="/AdminSignIn">
            <button>Admin Sign In</button>
          </Link> 

          <Switch> 
            <Route path="/Register" component={Register} />
            <Route path="/ForgotPassword" component={ForgotPassword} />
            <Route path="/SignIn" component={StorySelection} />
            <Route path="/AdminSignIn" component={AdminViewPage} />
          </Switch>

        </div>
      </Router>
    )
  }

}

export default Login;
