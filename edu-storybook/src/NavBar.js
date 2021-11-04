import React, { Component } from 'react'
import { Link } from "react-router-dom";

class NavBar extends Component {
    constructor() {
      super()
  
      this.state = {
        loggedIn: false
      }      
    }

render() {
  return (
    
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <Link className="navbar-brand nav-link" to="/">EduStorybook </Link>

        <ul class="navbar-nav ">
        {this.state.loggedIn ?
                  <React.Fragment>
                    <Link className='nav-link mr-3' to='/'>Log out</Link>
                    <Link className='nav-link' to="/StorySelection">Story Selection</Link>
                  </React.Fragment>
                  :
                  <React.Fragment>
                    <Link className='nav-link' to='/Login'>Log in</Link>
                    <Link className='nav-link' to='/Register'>Register</Link>
                  </React.Fragment>
                  }
        </ul>

      </nav>
      
  );
  
}
}
export default NavBar;
