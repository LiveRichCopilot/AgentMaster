import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar/Sidebar';
import ImageEditor from './pages/ImageEditor/ImageEditor';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/image-editor" element={<ImageEditor />} />
            {/* Define other routes here */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
