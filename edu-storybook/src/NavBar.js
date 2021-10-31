import React, { Component } from 'react'
import { Link } from "react-router-dom";

class NavBar extends Component {
    constructor() {
      super()
  
      this.state = {
        loggedIn: false
      }      
    }

    /* componentDidMount() {
      if (document.cookie.split(';').filter((item) => item.trim().startsWith('loggedIn=')).length) {
        this.setState({ loggedIn: true })
      }
      window.setInterval(() => {
        if (document.cookie.split(';').filter((item) => item.trim().startsWith('loggedIn=')).length) {
          this.setState({ loggedIn: true })
        }
        else {
          this.setState({ loggedIn: false })
        }
      }, 500)
    } */

render() {
  return (
    
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <li class="nav-item">
          <Link class="navbar-brand" to="/">EduStorybook </Link>
        </li>      

        <li class="nav-item">
          <Link class="nav-link" to="/">Home </Link>
        </li>

        <ul class="navbar-nav mr-auto">
        {this.state.loggedIn ?
                  <React.Fragment>
                    <Link className="nav-link mr-3" to="/myaccount">My account</Link>
                    <Link className='nav-link' to='/'>Log out</Link>
                    <Link className='nav-link' to="/StorySelection">Story Selection</Link>
                  </React.Fragment>
                  :
                  <React.Fragment>
                    <Link className='nav-link' to='/Login'>Log in</Link>
                    <Link className='nav-link' to='/Register'>Register</Link>
                  </React.Fragment>
                }

     { /*  <li class="nav-item">
          <Link class="nav-link" to="/Login">Login</Link>
        </li> 

        <li class="nav-item">
          <Link class="nav-link disabled" to="/StorySelection">Story Selection</Link>
              </li> */}

        </ul>

      </nav>
      
  );
  
}
}
export default NavBar;
