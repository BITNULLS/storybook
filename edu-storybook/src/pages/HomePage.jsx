import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class HomePage extends React.Component {

  render() {
    return <div className="HomePage">

      <p> Home Page </p>

      <Link to="/Login">Login</Link>
      <Link to="/Register">Register</Link>

    </div>;
  };

}
