import { useState } from "react";
import UploadContainer from "./components/UploadContainer";
import Navbar from "./components/Navbar";
import "./App.css";

function App() {
  // flex items-center justify-center
  return (
    <div className="min-h-screen  bg-stone-200">
      <Navbar />
      <div className="pt-15">
        <UploadContainer />
      </div>
    </div>
  );
}

export default App;
