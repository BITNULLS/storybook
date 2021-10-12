import React from "react";
import { Link } from "react-router-dom";

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
                
                <div class="form-group">
                  <button class="btn btn-primary" 
                    style = {{minWidth: 180, margin: 10}}>Upload New Book
                  </button >
                </div>
                
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
