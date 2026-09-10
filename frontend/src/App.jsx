import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    checking_status: '<0',
    duration: 12,
    credit_history: 'existing paid',
    purpose: 'radio/TV',
    credit_amount: 2500,
    savings_status: '<100',
    employment: '1<=X<4',
    installment_commitment: 2,
    personal_status: 'male single',
    other_parties: 'none',
    residence_since: 2,
    property_magnitude: 'real estate',
    age: 30,
    other_payment_plans: 'none',
    housing: 'own',
    existing_credits: 1,
    job: 'skilled',
    num_dependents: 1,
    own_telephone: 'yes',
    foreign_worker: 'yes'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? Number(value) : value
    });
  };

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
    <div className="dashboard-container">
      <header className="header">
        <h1> Enterprise Credit Risk Intelligence</h1>
        <p>AI-Powered Loan Default Assessment System (UCI Statlog Model)</p>
      </header>

      <div className="main-content">
        <form onSubmit={handleSubmit} className="form-card">
          <h3>Customer Financial & Credit Profile</h3>
          
          <div className="form-grid">
            <div className="input-group">
              <label>Checking Status</label>
              <select name="checking_status" value={formData.checking_status} onChange={handleChange}>
                <option value="<0">&lt; 0 DM</option>
                <option value="0<=X<200">0 &lt;= X &lt; 200 DM</option>
                <option value=">=200">&gt;= 200 DM</option>
                <option value="no checking">No Checking Account</option>
              </select>
            </div>

            <div className="input-group">
              <label>Duration (Months)</label>
              <input type="text" inputMode="numeric" name="duration" value={formData.duration} onChange={handleChange} required />
            </div>

            <div className="input-group">
              <label>Credit Amount ($)</label>
              <input type="text" inputMode="numeric" name="credit_amount" value={formData.credit_amount} onChange={handleChange} required />
            </div>

            <div className="input-group">
              <label>Age (Years)</label>
              <input type="text" inputMode="numeric" name="age" value={formData.age} onChange={handleChange} required />
            </div>

            <div className="input-group">
              <label>Savings Account/Bonds</label>
              <select name="savings_status" value={formData.savings_status} onChange={handleChange}>
                <option value="<100">&lt; 100 DM</option>
                <option value="100<=X<500">100 &lt;= X &lt; 500 DM</option>
                <option value="500<=X<1000">500 &lt;= X &lt; 1000 DM</option>
                <option value=">=1000">&gt;= 1000 DM</option>
                <option value="no savings">No Savings Account</option>
              </select>
            </div>

            <div className="input-group">
              <label>Credit History</label>
              <select name="credit_history" value={formData.credit_history} onChange={handleChange}>
                <option value="existing paid">Existing Paid</option>
                <option value="critical/other existing credit">Critical / Other Credits</option>
                <option value="delayed previously">Delayed Previously</option>
                <option value="no credits/all paid">No Credits / All Paid</option>
              </select>
            </div>

            <div className="input-group">
              <label>Housing</label>
              <select name="housing" value={formData.housing} onChange={handleChange}>
                <option value="own">Own</option>
                <option value="rent">Rent</option>
                <option value="for free">For Free</option>
              </select>
            </div>

            <div className="input-group">
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
            {loading ? 'Processing Model...' : 'Evaluate Credit Risk ⚡'}
          </button>
        </form>

        {result && (
          <div className={`result-card ${result.prediction_code === 1 ? 'status-good' : 'status-bad'}`}>
            <span className="badge">{result.prediction_code === 1 ? 'Approved' : 'High Risk'}</span>
            <h2>{result.prediction_label}</h2>
            <div className="metrics">
              <div className="metric-box">
                <small>Approval Probability</small>
                <strong>{result.confidence_good}</strong>
              </div>
              <div className="metric-box">
                <small>Default Risk Probability</small>
                <strong>{result.confidence_bad}</strong>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;