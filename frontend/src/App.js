import './App.css';
import React, { Component } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import HomepageLayout from './containers/Home';
import BaseRouter from "./routes";


class App extends Component {

  render() {
    return (
      <Router>
        <BaseRouter />
      </Router>
    );
  }
}

export default App;
