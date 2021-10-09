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
import { BrowserRouter, Route, NavLink, Switch, Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Navbar, Nav} from "react-bootstrap";


function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Navbar bg="light" expand="lg">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="/Login">Login</Nav.Link>
          <Nav.Link href="/StorySelection">Story Selection</Nav.Link>

       
        </Navbar>

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

/**
 *  <Link to="/">Home </Link>

        <Link to="/Login">Login</Link>
        <Link to="/StorySelection">Story Selection</Link>
 */