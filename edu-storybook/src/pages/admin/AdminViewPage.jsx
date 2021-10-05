import React, {useState} from "react";

/**
 * 
 * @returns 
 */
const AdminViewPage = (props) => {
  return( 
    <div>

      <p> Admin View Page </p>

      <button>Upload New Book</button><br />
      <button onClick={() => 
        props.history.push('/EditBook')
      }>Edit Book </button><br />
      <button>Add Users</button><br />
      <button>Download Data</button><br />

    </div>
  )

}

export default AdminViewPage;