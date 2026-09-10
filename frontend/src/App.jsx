import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    checking_status: '<0',
    duration: 48,
    credit_amount: 15000,
    age: 21,
    savings_status: '<100',
    credit_history: 'delayed previously',
    housing: 'rent',
    employment: 'unemployed'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle dynamic input changes
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? Number(value) : value
    });
  };

  // Process API request
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', { data: formData });
      setResult(response.data);
    } catch (error) {
      console.error("API Error:", error);
      alert("Error connecting to the risk engine server.");
    }
    setLoading(false);
  };

  return (
    <div className="fullscreen-layout">
      
      {/* --- TOP: Header --- */}
      <header className="app-header">
        <h1> Enterprise Credit Risk Intelligence</h1>
        <p>AI-Powered Loan Default Assessment System</p>
      </header>

      {/* --- BODY: Data Form & Results --- */}
      <main className="app-main">
        <div className="content-wrapper">
          
          {/* DATA INPUT FORM */}
          <form onSubmit={handleSubmit} className="wide-form">
            <div className="form-grid">
              
              <div className="input-field">
                <label>Checking Status</label>
                <select name="checking_status" value={formData.checking_status} onChange={handleChange}>
                  <option value="<0">&lt; 0 DM</option>
                  <option value="0<=X<200">0 &lt;= X &lt; 200 DM</option>
                  <option value=">=200">&gt;= 200 DM</option>
                  <option value="no checking">No Checking Account</option>
                </select>
              </div>

              <div className="input-field">
                <label>Duration (Months)</label>
                <input type="text" inputMode="numeric" name="duration" value={formData.duration} onChange={handleChange} required />
              </div>

              <div className="input-field">
                <label>Credit Amount ($)</label>
                <input type="text" inputMode="numeric" name="credit_amount" value={formData.credit_amount} onChange={handleChange} required />
              </div>

              <div className="input-field">
                <label>Age (Years)</label>
                <input type="text" inputMode="numeric" name="age" value={formData.age} onChange={handleChange} required />
              </div>

              <div className="input-field">
                <label>Savings Account/Bonds</label>
                <select name="savings_status" value={formData.savings_status} onChange={handleChange}>
                  <option value="<100">&lt; 100 DM</option>
                  <option value="100<=X<500">100 &lt;= X &lt; 500 DM</option>
                  <option value="500<=X<1000">500 &lt;= X &lt; 1000 DM</option>
                  <option value=">=1000">&gt;= 1000 DM</option>
                  <option value="no savings">No Savings Account</option>
                </select>
              </div>

              <div className="input-field">
                <label>Credit History</label>
                <select name="credit_history" value={formData.credit_history} onChange={handleChange}>
                  <option value="existing paid">Existing Paid</option>
                  <option value="critical/other existing credit">Critical / Other Credits</option>
                  <option value="delayed previously">Delayed Previously</option>
                  <option value="no credits/all paid">No Credits / All Paid</option>
                </select>
              </div>

              <div className="input-field">
                <label>Housing</label>
                <select name="housing" value={formData.housing} onChange={handleChange}>
                  <option value="own">Own</option>
                  <option value="rent">Rent</option>
                  <option value="for free">For Free</option>
                </select>
              </div>

              <div className="input-field">
                <label>Employment Since</label>
                <select name="employment" value={formData.employment} onChange={handleChange}>
                  <option value="unemployed">Unemployed</option>
                  <option value="<1">&lt; 1 Year</option>
                  <option value="1<=X<4">1 to 4 Years</option>
                  <option value="4<=X<7">4 to 7 Years</option>
                  <option value=">=7">&gt;= 7 Years</option>
                </select>
              </div>

            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Processing...' : 'Evaluate Credit Risk '}
            </button>
          </form>

          {/* RESULT BANNER */}
          {result && (
            <div className={`result-banner ${result.prediction_code === 1 ? 'banner-good' : 'banner-bad'}`}>
              <div className="result-info">
                <span className="badge">{result.prediction_code === 1 ? 'Approved' : 'High Risk'}</span>
                <h2>{result.prediction_label}</h2>
              </div>
              <div className="result-metrics">
                <div className="metric">
                  <small>Approval Prob.</small>
                  <strong>{result.confidence_good}</strong>
                </div>
                <div className="metric">
                  <small>Default Prob.</small>
                  <strong>{result.confidence_bad}</strong>
                </div>
              </div>
            </div>
          )}

        </div>
      </main>

      {/* --- FOOTER --- */}
      <footer className="app-footer">
        <p>Confidential & Proprietary © 2026 Ahmed Fekry | Designed for Enterprise Risk Management.</p>
      </footer>

    </div>
  );
}

export default App;