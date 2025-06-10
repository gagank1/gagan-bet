import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import './TempKeyLanding.css';

function TempKeyLanding() {
    const { key } = useParams();
    const [isLoading, setIsLoading] = useState(false);
    const [isValidKey, setIsValidKey] = useState(null); // null = checking, true = valid, false = invalid
    const [keyInfo, setKeyInfo] = useState(null);

    useEffect(() => {
        const validateKey = async () => {
            try {
                const response = await fetch(`/validatetempkey/${key}`);
                if (response.ok) {
                    const data = await response.json();
                    setIsValidKey(true);
                    setKeyInfo(data);
                } else {
                    setIsValidKey(false);
                    const data = await response.json();
                    toast.error(data.message || 'Invalid or expired temporary key', {
                        position: toast.POSITION.TOP_RIGHT
                    });
                }
            } catch (error) {
                setIsValidKey(false);
                toast.error('An error occurred while validating the key.', {
                    position: toast.POSITION.TOP_RIGHT
                });
            }
        };

        validateKey();
    }, [key]);

    const handleBuzzIn = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`/tempkey/${key}`);
            const data = await response.json();

            if (response.ok) {
                toast.success(data.message || 'Buzzed in successfully!', {
                    position: toast.POSITION.TOP_RIGHT
                });
                // Update remaining uses
                if (keyInfo) {
                    setKeyInfo(prev => ({
                        ...prev,
                        remaining_uses: prev.remaining_uses - 1
                    }));
                }
            } else {
                toast.error(data.message || 'Invalid or expired temporary key', {
                    position: toast.POSITION.TOP_RIGHT
                });
                setIsValidKey(false);
            }
        } catch (error) {
            toast.error('An error occurred while using the temporary key.', {
                position: toast.POSITION.TOP_RIGHT
            });
        } finally {
            setIsLoading(false);
        }
    };

    if (isValidKey === null) {
        return (
            <div className="temp-key-landing">
                <div className="landing-content">
                    <h1>Validating Key...</h1>
                    <p>Please wait while we check your access key.</p>
                </div>
            </div>
        );
    }

    if (!isValidKey) {
        return (
            <div className="temp-key-landing">
                <div className="landing-content">
                    <h1>Invalid Key</h1>
                    <p>This temporary access key is invalid or has expired.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="temp-key-landing">
            <div className="landing-content">
                <h1>Welcome!</h1>
                <p>You have a valid temporary access key.</p>
                {keyInfo && (
                    <div className="key-info">
                        <p>Remaining uses: {keyInfo.remaining_uses}</p>
                        <p>Expires: {new Date(keyInfo.expires_at).toLocaleString()}</p>
                    </div>
                )}
                <button 
                    onClick={handleBuzzIn}
                    disabled={isLoading}
                    className={isLoading ? 'loading' : ''}
                >
                    {isLoading ? 'Buzzing...' : 'Buzz In'}
                </button>
            </div>
        </div>
    );
}

export default TempKeyLanding; 