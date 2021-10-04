import React, {useState} from "react";
import EditBook from "./EditBook";
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function AdminViewPage(){

  return(
    <Router>
      <div>

        <p> Story Selection </p>

        <button>Upload New Book</button><br />
        <Link to="/EditBook">
          <button>EditBook</button>
        </Link><br />
        <button>Add Users</button><br />
        <button>Download Data</button><br />

        <Switch> 
          <Route exact path="/EditBook" component={EditBook} />
        </Switch>

      </div>
    </Router>
  )

}

export default AdminViewPage;