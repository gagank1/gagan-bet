import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes, Navigate, useNavigate } from 'react-router-dom';
import './App.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Zehra() {
  return (
    <div>
      <h1>HAPPY BIRTHDAY ZEHRA! ❤️</h1>
      <p>Don’t roast me but since I’m your beep boop 🙄 I thought it’d only be fitting if I made a beep boop card.</p>
      <p>It's hard to believe that it's been almost a year since we first crossed paths. Time feels like it’s flying by whenever we’re together. We just enter our own little weirdo universe, and it’s just perfect. You’re MY weirdo fr, and I feel so lucky that we share this special connection. I’m incredibly grateful for you and everything you do for me. All the sweet thoughtful things, and all ways you make me tweak too. Despite everything we’ve been through I love you more than ever. I love every minute I spend with you and I can’t wait to spend many, many more together.</p>
      <p>I hope your birthday is as extraordinary as you are baby.</p>
      <p>Love,</p>
      <p>Gagan</p>
      <img src="https://media.istockphoto.com/id/938480944/vector/panda-bear-illustration.jpg?s=612x612&w=0&k=20&c=eSaXCfW6D4hYwRYeTfyKDsxScRyJqZISk3DCV16AbFo=" alt="Your description" />
    </div>
  );
}

function PublicPage() {
  const [publicPassphrase, setPublicPassphrase] = useState('');
  const navigate = useNavigate();

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
        navigate('/zehra');
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
      <h1>Enter password to buzz in</h1>
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
      <h1>Reset public password</h1>
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
                <Link to="/public">Buzz in</Link>
              </li>
              <li>
                <Link to="/private">Admin</Link>
              </li>
            </ul>
          </nav>

          <Routes>
            <Route path="/public" element={<PublicPage/>} />
            <Route path="/private" element={<PrivatePage/>} />
            <Route path="/zehra" element={<Zehra/>} />
            <Route path="*" element={<Navigate to="/public" replace />} />
          </Routes>

        </div>
      </Router>
      <ToastContainer />
    </div>
  );
}

export default App;
