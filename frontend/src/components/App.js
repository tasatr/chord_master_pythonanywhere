import React, { Component } from "react";
import { usePromiseTracker } from "react-promise-tracker";
import { render } from "react-dom";
import HomePage from "./HomePage";

const LoadingIndicator = props => {
  const { promiseInProgress } = usePromiseTracker();

  return (
    promiseInProgress &&
    <h1>Hey some async call in progress ! </h1>
  );
}


export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <HomePage />
        <LoadingIndicator />
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);
