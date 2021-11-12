import React, { Component } from 'react'
import { Link } from "react-router-dom";

class NavBar extends Component {
  constructor() {
    super()

// both user/admin cannot be logged in at same time 
    this.state = {
      userLoggedIn: false,
      adminLoggedIn: true
    }
  }

  render() {
    return (

      <nav class="navbar navbar-expand-lg navbar-light bg-light">

        <Link className="navbar-brand nav-link" to="/">EduStorybook </Link>

        <ul class="navbar-nav">

          {this.state.userLoggedIn &&
            <React.Fragment>
              <Link className='nav-link mr-3' to='/'>Log out</Link>
              <Link className='nav-link' to="/StorySelection">Story Selection</Link>
            </React.Fragment>}

          {this.state.adminLoggedIn &&
            <React.Fragment>
              <Link className='nav-link mr-3' to='/'>Log out</Link>
              <Link className='nav-link' to="/StorySelection">Story Selection</Link>
              <Link className='nav-link' to="/AdminViewPage">Admin View</Link>
              <Link className='nav-link' to="/EditBook">Edit Book</Link>
            </React.Fragment>}

          {(!this.state.adminLoggedIn && !this.state.userLoggedIn) &&
            <React.Fragment>
              <Link className='nav-link' to='/Login'>Log in</Link>
              <Link className='nav-link' to='/Register'>Register</Link>
            </React.Fragment>}

        </ul>
      </nav>
    );
  }
}
export default NavBar;
