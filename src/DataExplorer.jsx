import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './DataExplorer.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const DataExplorer = ({ authorName = "Jone Mickel", onBack, onNavigateToSettings, onNavigateToAbout, onNavigateToProfile, onLogout, hasSearchedAuthor, onResetSearch, onNavigateToExplorer }) => {
  // State for filters
  const [selectedField, setSelectedField] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedHIndex, setSelectedHIndex] = useState('');
  const [selectedNmIndex, setSelectedNmIndex] = useState('');

  // Sample author data
  const authorData = {
    name: authorName,
    email: 'researcher@university.edu',
    totalPublications: 250,
    totalCitations: 250,
    totalSelfCitations: 250,
    nmIndex: 250,
    hIndex: 250,
    cScore: 250
  };

  // Sample chart data - Citations vs Publication Year
  const chartData = {
    labels: ['P', 'Q', 'R', 'S', 'T'],
    datasets: [
      {
        label: 'Citations',
        data: [220, 180, 240, 280, 260],
        borderColor: '#d32f2f',
        backgroundColor: 'rgba(211, 47, 47, 0.1)',
        tension: 0.4,
        pointRadius: 5,
        pointHoverRadius: 7
      },
      {
        label: 'Publications',
        data: [200, 240, 190, 230, 270],
        borderColor: '#034078',
        backgroundColor: 'rgba(3, 64, 120, 0.1)',
        tension: 0.4,
        pointRadius: 5,
        pointHoverRadius: 7
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 300,
        ticks: {
          stepSize: 50
        },
        grid: {
          color: '#e0e0e0'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  };

  // Sample publications data
  const publications = [
    {
      id: 1,
      title: 'Title of Publication',
      fields: ['Field 01', 'Field 02', 'Field 03', 'Field 04', 'Field 05'],
      authors: ['Mr. XXXX', 'Mr. YYYY', 'Mr. ZZZZ'],
      totalSelfCitations: 250,
      publishedYear: 250,
      totalCitations: 250
    },
    {
      id: 2,
      title: 'Title of Publication',
      fields: ['Field 01', 'Field 02', 'Field 03', 'Field 04', 'Field 05'],
      authors: ['Mr. XXXX', 'Mr. YYYY', 'Mr. ZZZZ'],
      totalSelfCitations: 250,
      publishedYear: 250,
      totalCitations: 250
    },
    {
      id: 3,
      title: 'Title of Publication',
      fields: ['Field 01', 'Field 02', 'Field 03', 'Field 04', 'Field 05'],
      authors: ['Mr. XXXX', 'Mr. YYYY', 'Mr. ZZZZ'],
      totalSelfCitations: 250,
      publishedYear: 250,
      totalCitations: 250
    }
  ];

  const handleExportCSV = () => {
    // Create CSV content
    const headers = ['Title', 'Fields', 'Authors', 'Total Self Citations', 'Published Year', 'Total Citations'];
    const csvContent = [
      headers.join(','),
      ...publications.map(pub => [
        `"${pub.title}"`,
        `"${pub.fields.join('; ')}"`,
        `"${pub.authors.join('; ')}"`,
        pub.totalSelfCitations,
        pub.publishedYear,
        pub.totalCitations
      ].join(','))
    ].join('\n');

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `${authorName}_publications.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="data-explorer-container">
      {/* Header */}
      <header className="data-explorer-header">
        <div className="header-left">
          <i className='bx bxs-graduation'></i>
          <h1 className="logo">ScholarMetrics</h1>
        </div>
        <div className="header-right">
          <nav className="header-nav">
            <a href="#dashboard" onClick={onBack} className="nav-link">Dashboard</a>
            {hasSearchedAuthor && (
              <a href="#explorer" className="nav-link active">Data Explorer</a>
            )}
            <a href="#about" className="nav-link" onClick={onNavigateToAbout}>About Us</a>
            <a href="#logout" className="nav-link" onClick={onLogout}>Logout</a>
          </nav>
          <div className="user-icon" onClick={onNavigateToProfile}>
            <i className='bx bxs-user-circle'></i>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="data-explorer-main">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h2 className="page-title">Data Explorer</h2>
          <button 
            onClick={() => { onResetSearch(); onBack(); }} 
            className="reset-search-btn"
            style={{
              padding: '0.625rem 1.25rem',
              background: 'var(--primary-color)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '0.875rem',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <i className='bx bx-reset'></i>
            Reset Search
          </button>
        </div>

        {/* Author Profile Section */}
        <section className="author-profile-section">
          <div className="profile-left">
            {/* Profile Card */}
            <div className="profile-card">
              <div className="profile-icon">
                <i className='bx bxs-user'></i>
              </div>
              <div className="profile-info">
                <h3>{authorData.name}</h3>
                <p>{authorData.email}</p>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="stats-grid-small">
              <div className="stat-item">
                <div className="stat-label">Total Publications</div>
                <div className="stat-value">{authorData.totalPublications}</div>
              </div>
              <div className="stat-item">
                <div className="stat-label">Total Citations</div>
                <div className="stat-value">{authorData.totalCitations}</div>
              </div>
              <div className="stat-item">
                <div className="stat-label">Total Self Citations</div>
                <div className="stat-value">{authorData.totalSelfCitations}</div>
              </div>
              <div className="stat-item">
                <div className="stat-label">Nm Index</div>
                <div className="stat-value">{authorData.nmIndex}</div>
              </div>
              <div className="stat-item">
                <div className="stat-label">H Index</div>
                <div className="stat-value">{authorData.hIndex}</div>
              </div>
              <div className="stat-item">
                <div className="stat-label">C Score</div>
                <div className="stat-value">{authorData.cScore}</div>
              </div>
            </div>
          </div>

          {/* Chart */}
          <div className="chart-container">
            <Line data={chartData} options={chartOptions} />
          </div>
        </section>

        {/* Filter Section */}
        <section className="filter-section">
          <div className="filter-header">
            <i className='bx bx-filter'></i>
            <span>Filter</span>
          </div>
          <div className="filter-controls">
            <div className="filter-item">
              <label>Field</label>
              <select 
                value={selectedField} 
                onChange={(e) => setSelectedField(e.target.value)}
              >
                <option value="">Select Field</option>
                <option value="medicine">Medicine</option>
                <option value="engineering">Engineering</option>
                <option value="psychology">Psychology</option>
              </select>
            </div>
            <div className="filter-item">
              <label>Year</label>
              <select 
                value={selectedYear} 
                onChange={(e) => setSelectedYear(e.target.value)}
              >
                <option value="">Select Year</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
              </select>
            </div>
            <div className="filter-item">
              <label>H-Index</label>
              <select 
                value={selectedHIndex} 
                onChange={(e) => setSelectedHIndex(e.target.value)}
              >
                <option value="">Nm-Index</option>
                <option value="high">High (&gt;100)</option>
                <option value="medium">Medium (50-100)</option>
                <option value="low">Low (&lt;50)</option>
              </select>
            </div>
            <div className="filter-item">
              <label>Nm-Index</label>
              <select 
                value={selectedNmIndex} 
                onChange={(e) => setSelectedNmIndex(e.target.value)}
              >
                <option value="">Nm-Index</option>
                <option value="high">High (&gt;100)</option>
                <option value="medium">Medium (50-100)</option>
                <option value="low">Low (&lt;50)</option>
              </select>
            </div>
          </div>
        </section>

        {/* Publications List */}
        <section className="publications-section">
          {publications.map((pub) => (
            <div key={pub.id} className="publication-card">
              <div className="publication-main">
                <h3 className="publication-title">{pub.title}</h3>
                <div className="publication-fields">
                  {pub.fields.map((field, index) => (
                    <span key={index} className="field-tag">{field}</span>
                  ))}
                </div>
                <div className="authors-section">
                  <h4>Authors Contribution</h4>
                  {pub.authors.map((author, index) => (
                    <p key={index}>{author}</p>
                  ))}
                </div>
              </div>
              <div className="publication-stats">
                <div className="pub-stat">
                  <div className="pub-stat-label">Total Self Citations</div>
                  <div className="pub-stat-value">{pub.totalSelfCitations}</div>
                </div>
                <div className="pub-stat">
                  <div className="pub-stat-label">Published Year</div>
                  <div className="pub-stat-value">{pub.publishedYear}</div>
                </div>
                <div className="pub-stat">
                  <div className="pub-stat-label">Total Citations</div>
                  <div className="pub-stat-value">{pub.totalCitations}</div>
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* Export Button */}
        <div className="export-section">
          <button className="export-btn" onClick={handleExportCSV}>
            Click here to Export CSV
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="data-explorer-footer">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-title">
              <i className='bx bx-file'></i>
              <h3>ScholarMetrics</h3>
            </div>
            <p>Revolutionizing research evaluation through intelligent automation and comprehensive data collection across global scholarly databases.</p>
          </div>

          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#dashboard">Dashboard</a></li>
              <li><a href="#explorer">Data Explorer</a></li>
              <li><a href="#settings">Settings</a></li>
              <li><a href="#about">About Us</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Resources</h4>
            <ul>
              <li><a href="#docs">Documentation</a></li>
              <li><a href="#api">API Reference</a></li>
              <li><a href="#tutorials">Tutorials</a></li>
              <li><a href="#faq">FAQ</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Contact</h4>
            <ul>
              <li><a href="#support">Support Center</a></li>
              <li><a href="mailto:info@academine.edu">info@academine.edu</a></li>
              <li><a href="#feedback">Send Feedback</a></li>
              <li><a href="#report">Report an Issue</a></li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default DataExplorer;
