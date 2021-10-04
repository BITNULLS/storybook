import React, {useState} from "react";
import AdminViewPage from "./AdminViewPage";
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function EditBook(){

  return(
    <Router>
      <div>

        <p> Edit Quizzes </p>

        <Link to="/AdminviewPage">
          <button>Admin View</button>
        </Link><br />
        <button>Save</button><br />

        <Switch> 
          <Route exact path="/AdminViewPage" component={AdminViewPage} />
        </Switch>
        
      </div>
    </Router>
  )

}

export default EditBook;
