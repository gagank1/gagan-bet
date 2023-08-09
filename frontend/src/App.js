import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import $ from 'jquery';

function PublicPage() {
  const [publicPassphrase, setPublicPassphrase] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission to your chosen URL
    const form_data = {
      public_passphrase: publicPassphrase
    }

    $.ajax({
      url: 'https://gagan.bet/buzzin',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(form_data),
      success: function (data) {
        console.log('Form submitted successfully');
      },
      error: function (error) {
        console.error('Form submission failed', error);
      },
    });

    console.log('Submitting public passphrase:', publicPassphrase);
  };

  return (
    <div>
      <h1>Public Passphrase</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={publicPassphrase}
          onChange={(e) => setPublicPassphrase(e.target.value)}
          placeholder="Enter public passphrase"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

function PrivatePage() {
  const [privatePassphrase, setPrivatePassphrase] = useState('');
  const [newPublicPassphrase, setNewPublicPassphrase] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission to your chosen URL
    const form_data = {
      private_passphrase: privatePassphrase,
      new_public_passphrase: newPublicPassphrase
    }

    $.ajax({
      url: 'https://gagan.bet/updatepublickey',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(form_data),
      success: function (data) {
        console.log('Form submitted successfully');
      },
      error: function (error) {
        console.error('Form submission failed', error);
      },
    });

    console.log('Submitting private passphrase:', privatePassphrase);
    console.log('Submitting new public passphrase:', newPublicPassphrase);
  };

  return (
    <div>
      <h1>Private Passphrase</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={privatePassphrase}
          onChange={(e) => setPrivatePassphrase(e.target.value)}
          placeholder="Enter private passphrase"
        />
        <input
          type="text"
          value={newPublicPassphrase}
          onChange={(e) => setNewPublicPassphrase(e.target.value)}
          placeholder="Enter new public passphrase"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Public Page</Link>
            </li>
            <li>
              <Link to="/private">Private Page</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<PublicPage/>} />
          <Route path="/private" element={<PrivatePage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
