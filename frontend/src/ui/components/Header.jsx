import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.css';

const logo = require('../assets/logo.png');

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className={styles.headerContainer}>
      {/* Top Header Bar */}
      <div className={styles.topBar}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <img
            src={logo}
            alt="Logo"
            className={styles.logo}
            onClick={() => navigate('/')} 
            style={{ cursor: 'pointer' }}
          />
        </div>

        <div className={styles.slogan}>license. create. attribute</div>
      </div>

      {/* Content Container */}
      <div className={styles.content}>
        {/* <input
          type="text"
          placeholder="Insert your API key here"
          className={styles.apiInput}
        /> */}

        {/* <a href="#" className={styles.link}>
          First time user? Get your key here
        </a> */}

        <p className={styles.infoText}>
          With Raily, as a content owner, you can control where your content is used and
          ensure it aligns with your terms. As a user, you can enjoy the content
          responsibly, respecting usage terms and avoiding unnecessary risks.{' '}
          <a href="#">learn more</a>
        </p>
      </div>
    </header>
  );
};

export default Header;
