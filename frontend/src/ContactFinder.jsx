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
      const response = await fetch('https://crawler-dreamskrin.onrender.com/extract-contacts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Server returned an error');
      }

      const data = await response.json();
      setContacts(data);
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to fetch contact information');
    } finally {
      setLoading(false);
    }
  };

  const LoadingSpinner = () => (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <span>Searching...</span>
    </div>
  );

  return (
    <div className="contact-finder-container">
      <div className="form-card">
        <h2 className="form-title">CrawlIt</h2>
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

        {error && <div className="error-message">{error}</div>}

        {loading && <LoadingSpinner />}

        {contacts && contacts.contactDetails && (
          <div className="contacts-section">
            <h3 className="contacts-title">Contact Information</h3>
            <div className="table-container">
              <table className="contact-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Email Address</td>
                    <td>{contacts.contactDetails.email || 'No email found'}</td>
                  </tr>
                  <tr>
                    <td>Phone Numbers</td>
                    <td>
                      {contacts.contactDetails.phoneNumbers &&
                      contacts.contactDetails.phoneNumbers.length > 0
                        ? contacts.contactDetails.phoneNumbers.map((phone, index) => (
                            <div key={index}>{phone}</div>
                          ))
                        : 'No phone numbers found'}
                    </td>
                  </tr>
                  {contacts.contactDetails.additionalContact && (
                    <tr>
                      <td>Additional Contact</td>
                      <td>{contacts.contactDetails.additionalContact}</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {contacts && (
          <div className="debug-section">
            <details>
              <summary>Show Raw Response</summary>
              <pre>{JSON.stringify(contacts, null, 2)}</pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContactFinder;