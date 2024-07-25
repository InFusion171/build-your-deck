import React from 'react';
import Navbar from "./container/navbar/navbar";
import Body from "./container/body/body";
import './App.css';

function App() {
  return (
    <div className="App">
      <div>
        <Navbar />
        <Body />
      </div>
    </div>
  );
}

export default App;
