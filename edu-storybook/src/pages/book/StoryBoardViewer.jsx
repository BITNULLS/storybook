import React, {useState} from "react";
import StorySelection from "../StorySelection";
import StoryBoardQuiz from "./StoryBoardQuiz";
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function StoryBoardViewer(){

  return(
    <Router>
      <div>

        <p> Storyboard Viewer </p>

        <Link to="/StorySelection">
          <button>Back to Story Selection</button>
        </Link>
        <button>Logout</button>

        <Switch> 
          <Route exact path="/StorySelection" component={StorySelection} />
        </Switch>
        
      </div>
    </Router>
  )

}

export default StoryBoardViewer;
