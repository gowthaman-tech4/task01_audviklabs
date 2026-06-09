import { useState, useEffect } from 'react';
import axios from 'axios';
import { Target, CheckCircle2, AlertTriangle, Shield, AlertCircle } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
  <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h3 style={{ color: 'var(--text-muted)', fontSize: '1rem', fontWeight: 500 }}>{title}</h3>
      <div style={{ padding: '8px', borderRadius: '8px', background: `rgba(${color}, 0.1)`, color: `rgb(${color})` }}>
        <Icon size={20} />
      </div>
    </div>
    <div>
      <div style={{ fontSize: '2.5rem', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '4px' }}>
        {value}
      </div>
      {subtitle && <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{subtitle}</div>}
    </div>
  </div>
);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEval = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/evaluation');
        if (response.data.error) {
          setError(response.data.error);
        } else {
          setData(response.data);
        }
      } catch (err) {
        setError("Failed to fetch evaluation metrics. Ensure backend is running and pipeline was evaluated.");
      } finally {
        setLoading(false);
      }
    };
    fetchEval();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div style={{ color: 'var(--danger)' }}><AlertCircle /> {error}</div>;
  if (!data) return null;

  const m = data.overall_metrics;
  
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Evaluation Dashboard</h1>
        <p className="page-subtitle">Overall performance metrics for the PII masking pipeline</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', marginBottom: '32px' }}>
        <StatCard 
          title="Accuracy (Recall)" 
          value={`${(m.accuracy * 100).toFixed(2)}%`}
          icon={Target}
          color="52, 211, 153"
          subtitle="Target: >95.00%"
        />
        <StatCard 
          title="Precision" 
          value={`${(m.precision * 100).toFixed(2)}%`}
          icon={Shield}
          color="96, 165, 250"
          subtitle="False positive resistance"
        />
        <StatCard 
          title="True Positives" 
          value={m.true_positives}
          icon={CheckCircle2}
          color="52, 211, 153"
          subtitle={`Out of ${m.total_ground_truth} entities`}
        />
        <StatCard 
          title="Missed (FN)" 
          value={m.false_negatives}
          icon={AlertTriangle}
          color="245, 158, 11"
          subtitle="Entities failed to mask"
        />
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ marginBottom: '24px' }}>Per-Type Performance</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)' }}>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>PII Type</th>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>TP</th>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>FP</th>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>FN</th>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Precision</th>
                <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Recall</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.by_type).map(([type, stats], i) => (
                <tr key={type} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '12px 8px' }}>
                    <span className="entity-highlight" data-type={type}>{type}</span>
                  </td>
                  <td style={{ padding: '12px 8px' }}>{stats.tp}</td>
                  <td style={{ padding: '12px 8px' }}>{stats.fp}</td>
                  <td style={{ padding: '12px 8px' }}>{stats.fn}</td>
                  <td style={{ padding: '12px 8px' }}>{(stats.precision * 100).toFixed(1)}%</td>
                  <td style={{ padding: '12px 8px', color: stats.recall < 0.9 ? 'var(--warning)' : 'inherit' }}>
                    {(stats.recall * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
