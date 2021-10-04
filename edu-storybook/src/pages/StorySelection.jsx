import React, {useState} from "react";
import StoryBoardViewer from "./book/StoryBoardViewer";
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function StorySelection(){

  return(
    <Router>
      <div>
      
        <p> Story Selection </p>

        <Link to="/StoryBoardViewer">
          <button>Read Now!</button>
        </Link>

        <Switch> 
          <Route exact path="/StoryBoardViewer" component={StoryBoardViewer} />
        </Switch>

      </div>
    </Router>
  )

}

export default StorySelection;
