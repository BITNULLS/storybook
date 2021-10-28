import React, {useState} from "react";
import { Link } from "react-router-dom";
//import {NavBar} from "bootstrap";
import {Container, Nav, NavDropdown,  Carousel} from "react-bootstrap";
import "./StoryBoardCSS/StoryBoardViewer.css";



/**
 * 
 * @returns 
 */

//TODO: Change "StoryViewer Title" to be Title of the current book
export default class StoryBoardViewer extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      story: "",
      pageNum: 0
    }

  }

//TODO: Change to call AJAX function to return page of the book from Database;
  // Question: is it going to be returned as URL or something different?
  async getImage(dir) {
    if( dir == "prev"){
      if(this.state.pageNum != 0){
        this.setState = {
          pageNum: -- this.state.pageNum
        }
      }
      else{
        alert("Please Stop")
        return
      }
    }
    else if( dir == "next"){
      this.setState ={
        pageNum: ++ this.state.pageNum
      }
    }
   
    var image = document.getElementById("testerPage");

    switch(this.state.pageNum) {
      case 0:
        image.src = "https://d28htnjz2elwuj.cloudfront.net/wp-content/uploads/2019/03/04120032/University-of-Delaware-400x400.jpg"
        break;
      case 1:
        image.src = "https://d28htnjz2elwuj.cloudfront.net/wp-content/uploads/2019/03/04120032/University-of-Delaware-400x400.jpg"
        break;
      case 2:
        image.src = process.env.PUBLIC_URL +'/images/Book.jpg'
        break;
      default:
        image.src = "https://i.pinimg.com/originals/4f/82/8d/4f828d05f82b8b7aedfe8be6a7d9d2a3.png"
        
    }
  }
  render() {
    return (
    <div>
      
      <p> Storyboard Viewer </p>
     
      <div id="homePage" class="carousel slide carousel-fade mx-auto" data-ride="inactive">
        <ol class="carousel-indicators">
          <li data-target="#homePage" data-slide-to="0" class="active"></li>
        </ol>
        <div class="carousel-inner" role="listbox">
          <div class="carousel-item active" data-interval="inactive">
            <img class="d-block w-100 h-75 mx-auto" src= {process.env.PUBLIC_URL +'/images/titlePage.png'} id="testerPage"
            alt="First Slide"/>
          </div>   
        </div>
      <a class="carousel-control-prev" href="#homePage" role="button" data-slide="prev" onClick={async () => {await this.getImage("prev")}}>
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#homePage" role="button" data-slide="next"  onClick={async () => {await this.getImage("next")}} >
          <span class="carousel-control-next-icon" aria-hidden="true"  ></span>
          <span class="sr-only">Next</span>
      </a>
      </div>

      <NavDropdown title = "Options">
        <NavDropdown.Item> <Link to="/StoryBoardQuiz">Go to Quiz</Link> </NavDropdown.Item>
        <NavDropdown.Item> <Link to="/StorySelection">Back to Story Selection</Link> </NavDropdown.Item>
      </NavDropdown>
     
    </div>
    )
  }

}

 