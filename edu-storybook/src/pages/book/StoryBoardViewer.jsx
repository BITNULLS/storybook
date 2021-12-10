import React, {useState} from "react";
import { Link } from "react-router-dom";
//import {NavBar} from "bootstrap";
import {Container, Nav, NavDropdown,  Carousel} from "react-bootstrap";
import "./StoryBoardCSS/StoryBoardViewer.css";
import $ from 'jquery';


/**
 * 
 * @returns 
 */

//TODO: Change "StoryViewer Title" to be Title of the current book
//TODO: Set to based on the book chosen by the user

export default class StoryBoardViewer extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      story: "Supporting Student Motivation in Online and Technology Concexts",
      bookId: 94, //Change to not hardcoded 
      pageNum: 0,
      pageCount:null
    }
  }

  componentDidMount() {
    fetch("/storyboard/pagecount/" + this.state.bookId)
      .then(response => response.json())
      .then(json => {
        this.setState({ pageCount: json.pagecount });
      });
  }
  
  
  async getImage(dir) {
    if( dir == "prev"){
      
      if(this.state.pageNum ==1){
        alert("Please Stop")
        return
      }
      else if(this.state.pageNum >1){
        this.setState = {
          pageNum: -- this.state.pageNum
        }
      }
      
    }
    else if( dir == "next"){
      if (this.state.pageNum == this.state.pageCount){
        alert("End of the storybook :)")
        return 
      }
      else {
        this.setState ={
          pageNum: ++ this.state.pageNum
        }
      }
    }
   
    if(this.state.pageNum>=1 &&  this.state.pageNum<= this.state.pageCount){
      var currImage = document.getElementById("testerPage");
      currImage.src = "/storyboard/page/" + this.state.bookId+ "/"+this.state.pageNum
      console.log(this.state.pageCount)
      console.log(currImage.src)
    }
  }
  render() {
    return (
    <div>
      
      <p> {this.story} </p>
     
      <div id="homePage" class="carousel slide carousel-fade mx-auto" data-ride="inactive">
        <ol class="carousel-indicators">
          <li data-target="#homePage" data-slide-to="0" class="active"></li>
        </ol>
        <div class="carousel-inner" role="listbox">
          <div class="carousel-item active" data-interval="inactive">
            <img class="img-fluid" src= {process.env.PUBLIC_URL +'/images/titlePage.png'} id="testerPage"
            alt="First Slide"/>
          </div>   
        </div>
      <a class="carousel-control-prev text-dark" href="#homePage" data-mdb-target="#carouselDarkVariant" role="button" data-slide="prev" onClick={async () => {await this.getImage("prev")}}>
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next text-dark" href="#homePage" data-mdb-target="#carouselDarkVariant" role="button" data-slide="next"  onClick={async () => {await this.getImage("next")}} >
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

 