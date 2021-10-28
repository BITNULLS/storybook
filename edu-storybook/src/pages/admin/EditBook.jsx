import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class EditBook extends React.Component {
  render() {
    return (
      <div>

        <div class="col">
          <h1 class="text-center mb-5">Edit Quiz</h1>

          <div id="homePage" class="carousel slide carousel-fade mx-auto" data-ride="carousel">
            <ol class="carousel-indicators">
              <li data-target="#homePage" data-slide-to="0" class="active"></li>
              <li data-target="#homePage" data-slide-to="1"></li>
              <li data-target="#homePage" data-slide-to="2"></li>
            </ol>

            <div class="carousel-inner" role="listbox">
              <div class="carousel-item active" data-interval="10000">
                <img class="d-block w-100 mx-auto" src= {process.env.PUBLIC_URL +'/images/titlePage.png'}
                alt="First Slide"/>
              </div>   

              <div class="carousel-item">
                <img class="d-block w-100 mx-center" src= {process.env.PUBLIC_URL +'/images/Book.jpg'}
                  alt="Second Slide"/>
                <div  id = "Purpose" class="carousel-caption d-none d-md-block mx-auto bg-transparent ">
                  <h1> The purpose of this website is to create an environment for learning 
                  and teaching current and future teachers to expand their knowledge</h1>
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
            
            <div className="text-center mt-5">
              <button class="btn btn-primary"
                style = {{minWidth: 180, margin: 10}}>Save
              </button >

              <button class="btn btn-primary"
                style = {{minWidth: 180, margin: 10}}>Publish
              </button >
            </div>

            <Link to="/AdminViewPage">Back to Admin View Page</Link>
      
          </div>

        </div>

      </div>
    )
    
  }

}
