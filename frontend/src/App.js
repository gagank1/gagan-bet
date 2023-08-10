import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function PublicPage() {
  const [publicPassphrase, setPublicPassphrase] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form_data = {
      "public_passphrase": publicPassphrase
    }

    try {
      const response = await fetch('/buzzin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(form_data),
      });
      const data = await response.json();

      if (response.ok) {
        // Display success toast with the message from the API response
        toast.success(data.message || 'POST request successful!', {
          position: toast.POSITION.TOP_RIGHT
        });
      } else {
        // Display error toast with the error message from the API response
        toast.error(data.message || 'POST request failed!', {
          position: toast.POSITION.TOP_RIGHT
        });
      }
    } catch (error) {
      // Display error toast for network or other errors
      toast.error('An error occurred while making the POST request.', {
        position: toast.POSITION.TOP_RIGHT
      });
    }
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form_data = {
      "private_passphrase": privatePassphrase,
      "new_public_passphrase": newPublicPassphrase
    }

    try {
      const response = await fetch('/updatepublickey', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(form_data),
      });
      const data = await response.json();

      if (response.ok) {
        // Display success toast with the message from the API response
        toast.success(data.message || 'POST request successful!', {
          position: toast.POSITION.TOP_RIGHT
        });
      } else {
        // Display error toast with the error message from the API response
        toast.error(data.message || 'POST request failed!', {
          position: toast.POSITION.TOP_RIGHT
        });
      }
    } catch (error) {
      // Display error toast for network or other errors
      toast.error('An error occurred while making the POST request.', {
        position: toast.POSITION.TOP_RIGHT
      });
    }
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
    <div>
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
      <ToastContainer />
    </div>
  );
}

export default App;
