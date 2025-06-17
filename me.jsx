import React from 'react';

const PhaseTwoPanel = () => {
  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>🚀 Phase Two Dashboard</h2>
      <p style={styles.text}>Welcome to the second phase of the project. Begin your exploration!</p>
      <button style={styles.button}>Launch Feature</button>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    margin: '2rem auto',
    maxWidth: '500px',
    backgroundColor: '#f4f4f4',
    borderRadius: '12px',
    boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
    textAlign: 'center'
  },
  heading: {
    fontSize: '24px',
    color: '#333'
  },
  text: {
    margin: '1rem 0',
    fontSize: '16px',
    color: '#555'
  },
  button: {
    padding: '0.6rem 1.2rem',
    fontSize: '16px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    borderRadius: '8px',
    cursor: 'pointer'
  }
};

export default PhaseTwoPanel;
