import logo from './logo.svg';
import './App.css';
import HomePage from "./pages/HomePage";
import Login from "./pages/login-register/Login";
import Register from "./pages/login-register/Register";
import ForgotPassword from "./pages/login-register/ForgotPassword";
import ResetPassword from "./pages/login-register/ResetPassword";
import StorySelection from "./pages/StorySelection"
import StoryBoardViewer from "./pages/book/StoryBoardViewer"
import StoryBoardQuiz from "./pages/book/StoryBoardQuiz"
import AdminViewPage from "./pages/admin/AdminViewPage"
import EditBook from "./pages/admin/EditBook"
import { BrowserRouter, Route, NavLink, Switch } from "react-router-dom";

function App() {
  return (
    /**<div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    <BrowserRouter>
        <div>

        <HomePage/>
            
            <Switch>
              <Route exact path="/HomePage"> <HomePage/> </Route>
           </Switch>
        </div> 
    </BrowserRouter>
*/
    <BrowserRouter>
      <div className="App">
        <NavLink exact activeClassName="active" to="/HomePage">Home </NavLink>
        <NavLink exact activeClassName="active" to="/Login">Login </NavLink>
        <NavLink exact activeClassName="active" to="/StorySelection">Story Selection </NavLink>

        <Switch>
            <Route exact path="/HomePage" component={HomePage} />
            <Route exact path="/Login" component={Login} />
            <Route path="/Register" component={Register} />
            <Route path="/ForgotPassword" component={ForgotPassword} />
            <Route path="/ResetPassword" component={ResetPassword} />
            <Route path="/StorySelection" component={StorySelection} />
            <Route path="/StoryBoardViewer" component={StoryBoardViewer} />
            <Route path="/StoryBoardQuiz" component={StoryBoardQuiz} />
            <Route path="/AdminViewPage" component={AdminViewPage} />
            <Route path="/EditBook" component={EditBook} />

        </Switch>
      </div>
    </BrowserRouter>

  );
}

export default App;
