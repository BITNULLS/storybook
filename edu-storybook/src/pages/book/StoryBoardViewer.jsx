import React, {useState} from "react";
import { Link } from "react-router-dom";
//import {NavBar} from "bootstrap";
import {Container, Nav, NavDropdown,  Carousel} from "react-bootstrap";
import "./StoryBoardCSS/StoryBoardViewer.css";
/**
 * 
 * @returns 
 */
export default class StoryBoardViewer extends React.Component {
    render() {
    return <div>


      <p> Storyboard Viewer </p>
     
      <ControlPage />
     
      <NavDropdown title = "Options">
     


        <NavDropdown.Item> <Link to="/StoryBoardQuiz">Go to Quiz</Link> </NavDropdown.Item>
        <NavDropdown.Item> <Link to="/StorySelection">Back to Story Selection</Link> </NavDropdown.Item>
    </NavDropdown>
    </div>
  }

}

function ControlPage(){
  
  const [index, setIndex] = useState(0);


  function handleLeft(e) {
    e.preventDefault();
//    index = index +1;
    setIndex(index +1);
    getImage(index);
    console.log(index, "hi");
    //console.log('You clicked submit.');
  }

  function handleRight(e) {
    e.preventDefault();
    if(index != 0){
    setIndex(index -1);
    getImage(index);
    console.log(index, "hi");
    //console.log('You clicked submit.');
    }
    else {
      alert("PleaseStop");
    }
  }

/**  useEffect(() => {
    // Update the document title using the browser API
    document.image = `You clicked ${count} times`;
  });
*/

  return(
    <div>
      <button onClick = {handleRight}>
        Previous
      </button>

      <img className ="storyPage" src = "https://d28htnjz2elwuj.cloudfront.net/wp-content/uploads/2019/03/04120032/University-of-Delaware-400x400.jpg"  id = "testerPage">
      </img>
      <button  onClick = {handleLeft}>
        Next
      </button>
    </div>

  )

}
//

  function getImage(props){
    const index = props;
   
    var image = document.getElementById("testerPage");

  

    switch(index) {
      case 0:
        image.src = "https://d28htnjz2elwuj.cloudfront.net/wp-content/uploads/2019/03/04120032/University-of-Delaware-400x400.jpg"
        break;
      case 1:
        image.src = "https://d28htnjz2elwuj.cloudfront.net/wp-content/uploads/2019/03/04120032/University-of-Delaware-400x400.jpg"
        break;
      case 2:
      image.src = "https://marvel-b1-cdn.bc0a.com/f00000000164722/www.udel.edu/content/udel/en/faculty-staff/human-resources/benefits/enrollment/_jcr_content/par_udel_panel/image.img.jpg/1621437665944.jpg";
        break;
      default:
        image.src = "https://i.pinimg.com/originals/4f/82/8d/4f828d05f82b8b7aedfe8be6a7d9d2a3.png"
        
    }

    return(
      
    
        console.log(index)
  
      )
    
  }
