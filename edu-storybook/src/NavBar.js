import React, { Component } from 'react'
import { Link } from "react-router-dom";

class NavBar extends Component {

render() {
  return (
  <nav class="navbar navbar-expand-lg navbar-light bg-light">

        <li class="nav-item">
          <Link class="navbar-brand" to="/">EduStorybook </Link>
        </li>      

        <ul class="navbar-nav mr-auto">
        
        <li class="nav-item active">
          <Link class="nav-link" to="/">Home </Link>
        </li>

        <li class="nav-item">
          <Link class="nav-link" to="/Login">Login</Link>
        </li>

        <li class="nav-item">
          <Link class="nav-link disabled" to="/StorySelection">Story Selection</Link>
        </li>

        </ul>

      </nav>
  );
}
}
export default NavBar;
