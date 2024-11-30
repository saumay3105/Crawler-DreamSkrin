import React, { useState } from 'react';
import './ContactFinder.css'
const ContactFinder = () => {
  const [url, setUrl] = useState('');
  const [contacts, setContacts] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/extract-contacts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      console.log('Received data:', data);
      setContacts(data);
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to fetch contact information');
    } finally {
      setLoading(false);
    }
  };


  console.log('Current contacts state:', contacts);

  return (
    <div className="contact-finder-container">
      <div className="form-card">
        <h2 className="form-title">Website Contact Finder</h2>
        <form onSubmit={handleSubmit} className="form">
          <input
            type="url"
            placeholder="Enter website URL..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="form-input"
            required
          />
          <button type="submit" className="form-button" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {contacts && contacts.contactDetails && (
          <div className="contacts-section">
            <h3 className="contacts-title">Contact Information</h3>
            <div className="contacts-grid">
              <div className="contact-column">
                <h4 className="column-title">Email Address</h4>
                <div className="contact-item">
                  {contacts.contactDetails.email || 'No email found'}
                </div>
              </div>
              <div className="contact-column">
                <h4 className="column-title">Phone Numbers</h4>
                {contacts.contactDetails.phoneNumbers && 
                 contacts.contactDetails.phoneNumbers.length > 0 ? (
                  contacts.contactDetails.phoneNumbers.map((phone, index) => (
                    <div key={index} className="contact-item">
                      {phone}
                    </div>
                  ))
                ) : (
                  <div className="contact-item">No phone numbers found</div>
                )}
              </div>
            </div>
          </div>
        )}

        
        <div className="debug-section" style={{ marginTop: '20px', textAlign: 'left' }}>
          <p>Raw Response:</p>
          <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
            {JSON.stringify(contacts, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default ContactFinder;