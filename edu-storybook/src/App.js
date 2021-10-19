import logo from './logo.svg';
import './App.css';
import HomePage from "./pages/HomePage";
import Login from "./pages/login-register/Login";
import 'bootstrap/dist/css/bootstrap.min.css';
import Register from "./pages/login-register/Register";
import ForgotPassword from "./pages/login-register/ForgotPassword";
import ResetPassword from "./pages/login-register/ResetPassword";
import StorySelection from "./pages/StorySelection"
import StoryBoardViewer from "./pages/book/StoryBoardViewer"
import StoryBoardQuiz from "./pages/book/StoryBoardQuiz"
import AdminViewPage from "./pages/admin/AdminViewPage"
import EditBook from "./pages/admin/EditBook"
import { BrowserRouter, Route, NavLink, Switch, Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <BrowserRouter>
    
    <div className="App">
      <nav  class="navbar navbar-expand-lg navbar-light bg-light">
        <li class="nav-item">
          <Link class="navbar-brand" to="/">EduStorybook </Link>
        </li>      

        <ul class="navbar-nav mr-auto">
        
        <li class="nav-item active">
          <Link class="nav-link" to="/">Home </Link>
        </li>
        <li class="nav-item">
          <Link class="nav-link" to="/Login">Login</Link>
        </li>
        <li class="nav-item">
          <Link class="nav-link disabled" to="/StorySelection">Story Selection</Link>
        </li>
        </ul>
       
      </nav>

        <Switch>
          <Route exact path="/">
            <HomePage />
          </Route>
          <Route path="/Login">
            <Login />
          </Route>
          <Route path="/Register">
            <Register />
          </Route>
          <Route path="/ForgotPassword">
            <ForgotPassword />
          </Route>
          <Route path="/ResetPassword">
            <ResetPassword />
          </Route>
          <Route path="/StorySelection">
            <StorySelection />
          </Route>
          <Route path="/StoryBoardViewer">
            <StoryBoardViewer />
          </Route>
          <Route path="/StoryBoardQuiz">
            <StoryBoardQuiz />
          </Route>
          <Route path="/AdminViewPage">
            <AdminViewPage />
          </Route>
          <Route path="/EditBook">
            <EditBook />
          </Route>
        </Switch>
      </div>
    </BrowserRouter>

  );
}

export default App;

