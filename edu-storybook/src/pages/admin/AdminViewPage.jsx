import React from "react";
import { Link } from "react-router-dom";
import $ from 'jquery';

/**
 * 
 * @returns 
 */
 export default class AdminViewPage extends React.Component {
  render() { 
    return (

      <div class="row mt-5">
        <div class="col-12 col-md-4 col-sm-3"></div>
        <div class="col">
          <h1 class="text-center mb-5">Admin View</h1>

          <div class="card pl-1 pr-1">
            <div class="card-body">
              <form>
                


              <div id="file-content" onSubmit={e => e.preventDefault()}>
                  <input id="file" type="file" accept="pdf/*" hidden="true" />
                    <label htmlFor="file">
                      <span
                        id="file-upload-btn" 
                        class="btn btn-primary"
                        style = {{minWidth: 180, margin: 10}}>Upload New Book
                      </span>
                    </label>
                </div>

                
                
                <div action="http://localhost:5000/admin/book/upload">
                  <label for="file">Select a file:</label>
                  <input type="file" id="file" name="file" hidden="true"/><br></br>
                  <input type="submit" onClick={
                    function uploadingBook(e) {
                      e.preventDefault();
                      let file = $('#file').val()
                      console.log(file)
                      console.log("in new uploading")
                      if (file != 0) {
                        try {

                          $.post("http://localhost:5000/admin/book/upload", 
                            {data: file}, 
                            function(data, status, xhr) {
                              console.log("inside function in post")
                              console.log(data)
                              console.log("here")
                              new AdminViewPage(file)
                              alert("Successfully uploaded book: " + file)
                              console.log("after uploading function")
                            }, 'pdf');

                          console.log("before admin view page function")
                          new AdminViewPage(file)
                          console.log("after posting function")
                        }
                        catch {
                          alert("Unable to upload " + file + " Please try again.")
                          console.log("uploading did not work, error caught")
                        }
                      } else {
                        alert("Unable to upload " + file + " Please try again.")
                      }
                    }
                  }/>
                </div>
               
                



                { <div class="form-group" onSubmit={e => e.preventDefault()}>
                
                  <button id="load_file" onClick={
                    function sendFileRequest() {
                      let file = $('#file').val()
                      console.log(file)
                      console.log("before ajax")

                      

                      $.ajax({
                        url: "http://localhost:5000/admin/book/upload",
                        type: "POST",
                        dataType: 'pdf',
                        data: {file},
                        processData: false,
                        contentType: "application/x-www-form-urlencoded",
                        success: function(data){
                          console.log("inside success")
                          new AdminViewPage(data)
                          console.log("after book has uploaded through backend")
                          alert("Successfully uploaded new book!" )
                        },
                        error: function() {
                          console.log("did not upload properly")
                          alert("Unable to upload new book. Please try again. ")
                        }, 
                    });
                  }
                  }>Upload Book</button >
                
              </div> }

                



                





                    
                <div class="form-group">             
                  <Link to="/EditBook">
                    <button class="btn btn-primary"
                      style = {{minWidth: 180, margin: 10}}>Edit Book
                    </button >
                  </Link>
                </div>

                <div class="form-group">
                  <button class="btn btn-primary"
                    style = {{minWidth: 180, margin: 10}}>Add Users
                  </button >
                </div>

                <div class="form-group">
                  <button class="btn btn-primary"
                    style = {{minWidth: 180, margin: 10}}>Download Data
                  </button >
                </div>

              </form>
            </div >
          </div>
        </div >
        <div class="col col-12 col-md-4 col-sm-3"></div>
      </div >

    )
  }
}
