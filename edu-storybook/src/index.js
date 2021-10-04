import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Switch } from "react-router-dom";

import HomePage from "./pages/HomePage";
import Login from "./pages/login-register/Login";

const rootElement = document.getElementById("root");
ReactDOM.render(
  <BrowserRouter>
     <Switch>
       <Route exact path="/HomePage" component={HomePage} />
        <Route exact path="/Login" component={Login} />
     </Switch>
  </BrowserRouter>,
  rootElement
);
/** 
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
*/

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
