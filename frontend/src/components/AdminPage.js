import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminPage.css';

function AdminPage() {
    const [privateKey, setPrivateKey] = useState('');
    const [newKey, setNewKey] = useState(null);
    const [activeKeys, setActiveKeys] = useState([]);
    const [formData, setFormData] = useState({
        expiration_hours: 24,
        max_uses: 1,
        note: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Add polling interval state
    const [pollingInterval, setPollingInterval] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const fetchActiveKeys = async () => {
        try {
            const response = await axios.get(`/listtempkeys?private_passphrase=${privateKey}`);
            // Sort keys by creation date, most recent first
            const sortedKeys = response.data.active_keys.sort((a, b) => 
                new Date(b.created_at) - new Date(a.created_at)
            );
            setActiveKeys(sortedKeys);
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to fetch active keys');
            setIsAuthenticated(false);
            setActiveKeys([]);
            // Stop polling if we get an error
            if (pollingInterval) {
                clearInterval(pollingInterval);
                setPollingInterval(null);
            }
        }
    };

    const handleAuthSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        
        try {
            await fetchActiveKeys();
            setIsAuthenticated(true);
            setError('');
            
            // Start polling when authenticated
            const interval = setInterval(fetchActiveKeys, 5000); // Poll every 5 seconds
            setPollingInterval(interval);
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to authenticate');
            setIsAuthenticated(false);
            setActiveKeys([]);
        }
    };

    // Cleanup polling on component unmount
    useEffect(() => {
        return () => {
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
        };
    }, [pollingInterval]);

    const createTempKey = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        
        try {
            const response = await axios.post('/createtempkey', {
                private_passphrase: privateKey,
                ...formData
            });
            setNewKey(response.data.temp_key);
            setSuccess('Temporary key created successfully!');
            fetchActiveKeys();
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to create temporary key');
        }
    };

    const deleteTempKey = async (key) => {
        setError('');
        setSuccess('');
        
        try {
            await axios.delete(`/deletetempkey/${key}?private_passphrase=${privateKey}`);
            setSuccess('Temporary key deleted successfully!');
            fetchActiveKeys();
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to delete temporary key');
        }
    };

    return (
        <div className="admin-page">
            <h1>Admin Dashboard</h1>
            
            {!isAuthenticated ? (
                <div className="private-key-section">
                    <form onSubmit={handleAuthSubmit}>
                        <input
                            type="password"
                            placeholder="Enter private key"
                            value={privateKey}
                            onChange={(e) => setPrivateKey(e.target.value)}
                        />
                        <button type="submit">Authenticate</button>
                    </form>
                </div>
            ) : (
                <>
                    <div className="create-key-section">
                        <h2>Create New Temporary Key</h2>
                        <form onSubmit={createTempKey}>
                            <div className="form-group">
                                <label>Expiration (hours):</label>
                                <input
                                    type="number"
                                    name="expiration_hours"
                                    value={formData.expiration_hours}
                                    onChange={handleInputChange}
                                    min="1"
                                />
                            </div>
                            <div className="form-group">
                                <label>Maximum Uses:</label>
                                <input
                                    type="number"
                                    name="max_uses"
                                    value={formData.max_uses}
                                    onChange={handleInputChange}
                                    min="1"
                                />
                            </div>
                            <div className="form-group">
                                <label>Note/Label:</label>
                                <input
                                    type="text"
                                    name="note"
                                    value={formData.note}
                                    onChange={handleInputChange}
                                    placeholder="e.g., Delivery driver John"
                                />
                            </div>
                            <button type="submit">Create Key</button>
                        </form>
                    </div>

                    {newKey && (
                        <div className="new-key-section">
                            <h3>New Temporary Key Created</h3>
                            <p>Share this URL with the recipient:</p>
                            <code>{`${window.location.origin}/tempkeylanding/${newKey}`}</code>
                        </div>
                    )}

                    <div className="active-keys-section">
                        <h2>Active Temporary Keys</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Key</th>
                                    <th>Note</th>
                                    <th>Created</th>
                                    <th>Expires</th>
                                    <th>Remaining Uses</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {activeKeys.map(key => (
                                    <tr key={key.key}>
                                        <td>{key.key}</td>
                                        <td>{key.note}</td>
                                        <td>{new Date(key.created_at).toLocaleString()}</td>
                                        <td>{new Date(key.expires_at).toLocaleString()}</td>
                                        <td>{key.remaining_uses}</td>
                                        <td>
                                            <button 
                                                onClick={() => deleteTempKey(key.key)}
                                                className="delete-button"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </>
            )}

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
        </div>
    );
}

export default AdminPage; 