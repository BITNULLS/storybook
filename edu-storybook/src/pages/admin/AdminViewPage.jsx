import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
 export default class AdminViewPage extends React.Component {
  render() { 
    return <div>

      <p> Admin View Page </p>

      <button>Upload New Book</button><br />
      <Link to="/EditBook">Edit Book</Link>
      <button>Add Users</button><br />
      <button>Download Data</button><br />

    </div>;
  }

}
