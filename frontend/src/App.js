import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AdminPage from './components/AdminPage';
import TempKeyLanding from './components/TempKeyLanding';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <ToastContainer />
        <Routes>
          <Route path="/" element={<AdminPage />} />
          <Route path="/tempkeylanding/:key" element={<TempKeyLanding />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
