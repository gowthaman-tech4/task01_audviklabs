import { useState } from 'react';
import { ShieldCheck, Activity, FileText } from 'lucide-react';
import Dashboard from './components/Dashboard';
import LiveMasking from './components/LiveMasking';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('live');

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <ShieldCheck size={28} />
          <span>Audvik Security</span>
        </div>
        
        <nav className="nav-links">
          <div 
            className={`nav-link ${activeTab === 'live' ? 'active' : ''}`}
            onClick={() => setActiveTab('live')}
          >
            <FileText size={20} />
            <span>Live Masking</span>
          </div>
          <div 
            className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <Activity size={20} />
            <span>Evaluation Dashboard</span>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'live' && <LiveMasking />}
        {activeTab === 'dashboard' && <Dashboard />}
      </main>
    </div>
  );
}

export default App;
