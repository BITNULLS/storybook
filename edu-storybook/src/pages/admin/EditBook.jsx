import React from "react";
import { Link } from "react-router-dom";

/**
 * 
 * @returns 
 */
export default class EditBook extends React.Component {
  render() {
    return <div>

      <p> Edit Quizzes </p>

      <Link to="/AdminViewPage">Back to Admin View Page</Link>

      <button>Save </button>
      <button>Publish </button>

      </div>;
  }

}
