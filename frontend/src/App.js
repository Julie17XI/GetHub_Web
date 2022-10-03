import './App.css';
import React, {useState, useEffect} from 'react';
import {BrowserRouter as Router} from "react-router-dom";
import CustomTitle from './components/CustomTitle';
import Header from './components/Header';
import Body from './components/Body';
import axios from 'axios';

/**
 * Component to get input username and display the information for a given username
 * @param {null}
 * @return {HTML} <Router><Router/>
 * @example
 *    App()
 */
const App = () => {
  const [title, setTitle] = CustomTitle("GetHub")
  const [searchInput, setSearchInput] = useState("");
  const [searchResult, setSearchResult] = useState(null);

  const changeSearchResult = (result) => {
    setSearchResult(result);
  }

  return (
    <Router>
      <Header
      searchInput={searchInput}
      setSearchInput={setSearchInput}
      changeSearchResult={changeSearchResult}
      />
      <Body
      searchResult={searchResult}
      />
    </Router>
  );
}

export default App;
