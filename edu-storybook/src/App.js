import logo from './logo.svg';
import './App.css';
import HomePage from "./pages/HomePage";
import Login from "./pages/login-register/Login";
import Register from "./pages/login-register/Register";
import { BrowserRouter, Router, Route, Link, NavLink, Switch, Redirect } from "react-router-dom";

function App() {
  return (
    /**<div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    <BrowserRouter>
        <div>

        <HomePage/>
            
            <Switch>
              <Route exact path="/HomePage"> <HomePage/> </Route>
           </Switch>
        </div> 
    </BrowserRouter>
*/
    <BrowserRouter>
      <div>
        <HomePage/>
      </div>
    </BrowserRouter>

  );
}

export default App;
