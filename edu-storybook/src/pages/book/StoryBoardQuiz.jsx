import React, {useState} from "react";
import StoryBoardViewer from "./StoryBoardViewer";
import HomePage from "../HomePage";
import { BrowserRouter as Router, Route, Link, NavLink, Switch } from "react-router-dom";

/**
 * 
 * @returns 
 */
function StoryBoardQuiz(){

  return(
    <Router>
      <div>

        <p> Storyboard Quiz Viewer </p>

        <Link to="/StoryBoardViewer">
          <button>Back to StoryBoard Viewer</button>
        </Link>
        <Link to="/HomePage">
          <button>Logoutr</button>
        </Link>

        <Switch> 
          <Route exact path="/StoryBoardViewer" component={StoryBoardViewer} />
          <Route exact path="/HomePage" component={HomePage} />
        </Switch>
        
      </div>
    </Router>
  )

}

export default StoryBoardQuiz;
