import React, {useState} from "react";
import Login from "./login-register/Login";
import Register from "./login-register/Register";
import { BrowserRouter, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function HomePage() {

  return(
      <BrowserRouter>
        <div className="HomePage">
          <p> Home Page </p>

          <Link to="/Login">
            <button>Login</button>
          </Link>

          <Link to="/Register">
            <button>Register</button> 
          </Link>

          <Switch>
            <Route path="/Login" component={Login} />
            <Route path="/Register" component={Register} />
          </Switch> 

        </div> 
    </BrowserRouter>

          
  )

}

export default HomePage;



/**

<Link to="/Login">
            <button>Login</button>
          </Link>

          <Link to="/Register">
            <button>Register</button> 
          </Link>

          <Switch> 
            <Route path="/Login" component={Login} />
            <Route path="/Register" component={Register} />
          </Switch> */
/**

          <Link to="/Login">
            <button>Login</button>
          </Link>

          <Link to="/Register">
            <button>Register</button> 
          </Link>

          <Switch> 
            <Route path="/Login" component={Login} />
            <Route path="/Register" component={Register} />
          </Switch> */