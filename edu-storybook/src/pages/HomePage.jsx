import React from "react";
import { Link } from "react-router-dom";
import titlePage  from "../images/TitlePage.png";
import "./home-carousel.css";
import bookCover from "../images/Book.jpg";
import chalkboard from "../images/Chalkboard.jpg";


/**
 * Displays the 'login' & 'register' fields in order to send user to them. 
 * Add backend:
 * Add: if user is not logged in / they cannot read
 * 
 * Carousel of overview: 1) img of one book 
 *                       2) what the website is for educational purposes 
 *                       3) Get Started with your learning / include Login  
 */


export default class HomePage extends React.Component {

  render() {

    return (
    <div className="HomePage">
      <h1 className="text-center mb-5">Welcome to EduStorybook </h1>
      <div id="homePage" class="carousel slide carousel-fade mx-auto" data-ride="carousel">
        <ol class="carousel-indicators">
          <li data-target="#homePage" data-slide-to="0" class="active"></li>
          <li data-target="#homePage" data-slide-to="1"></li>
          <li data-target="#homePage" data-slide-to="2"></li>
        </ol>
        <div class="carousel-inner" role="listbox">
          <div class="carousel-item active" data-interval="10000">
            <img class="d-block w-100 mx-auto" src={titlePage}
            alt="First slide"/>
          </div>   
          <div class="carousel-item">
            <img class="d-block w-100 mx-center" src= {bookCover}
              alt="Second slide"/>
            <div  id = "Purpose" class="carousel-caption d-none d-md-block mx-auto bg-transparent ">
              <h1> The purpose of this website is to create an environment for learning 
               and teaching current and future teachers to expand their knowledge</h1>
            </div>
          </div>
          <div class="carousel-item">
            <img class="d-block w-100 mx-center" src = {chalkboard}
            alt="Third Slide"/>
          <div  id = "LogReg" class="carousel-caption d-none d-md-block mx-auto bg-transparent mx-center ">
            <h1> Have an account? Still need to Register?  </h1>
              <Link to="/Login" class="btn btn-link">Login</Link>
              <Link to="/Register" class="btn btn-link">Register</Link>
            </div>
          </div>
        </div>
  
        <a class="carousel-control-prev" href="#homePage" role="button" data-slide="prev" onclick="$('#homePage').carousel('prev')">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#homePage" role="button" data-slide="next" onclick="$('#homePage').carousel('prev')">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="sr-only">Next</span>
        </a>
      </div>

      <div className="text-center mt-5">
        <Link to="/Login" className="btn btn-link">Login</Link>     
        <Link to="/Register" className="btn btn-link">Register</Link>
      </div>

    </div>
    )
  };

}
