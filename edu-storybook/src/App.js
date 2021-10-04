import logo from './logo.svg';
import './App.css';
import HomePage from "./pages/HomePage";
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
    </div>*/
    <BrowserRouter>
      <div>
        
        <Route exact path="/"> 
          <Redirect to="/HomePage" component={HomePage} />
        </Route>

      </div>
    </BrowserRouter>
  );
}

export default App;
