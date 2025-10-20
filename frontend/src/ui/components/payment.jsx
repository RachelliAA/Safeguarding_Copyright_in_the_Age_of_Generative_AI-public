import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './Payment.module.css';

const Payment = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { imageData } = location.state || {};

  if (!imageData) {
    return <div>No image available. Please generate one first.</div>;
  }

  const handlePayClick = (e) => {
    e.preventDefault();
    navigate("/good-picture", { state: { imageData } });
  };

  
  const handleBackClick = (e) => {
    e.preventDefault();
    navigate(-1); // This goes back one page in the browser history
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.text}>License this image</div>
        <img src={imageData} alt="Preview" className={styles.image} />
      </div>

      <div className={styles.summaryBox}>
        <div className={styles.summaryRow}>
          <p className={styles.label}>You're paying</p>
          <h2 className={styles.amount}>$1.00</h2>
        </div>

        <div className={styles.descriptionRow}>
          <p className={styles.description}>1 image, licensed from Naruto</p>
          <p className={styles.description}>$1.00</p>
        </div>
        <p className={styles.subtext}>Personal license, non-commercial</p>

        <div className={styles.summaryRow}>
          <p className={styles.lineItem}>Discounts & Offers:</p>
          <p className={styles.lineItem}>$0.00</p>
        </div>

        <hr />

        <div className={styles.summaryRow}>
          <p className={styles.lineItem}>Tax:</p>
          <p className={styles.lineItem}>$0.00</p>
        </div>

        <div className={styles.summaryRow}>
          <p className={styles.total}>Total:</p>
          <p className={styles.total}>$1.00</p>
        </div>
      </div>

      <div className={styles.form} >
        <input name="name" placeholder="Credit card holder's name" />
        <input name="cardNumber" placeholder="Credit card number" />
        <div className={styles.row}>
          <input name="expiry" placeholder="MM/YY" style={{ flex: 1 }} />
          <input name="cvc" placeholder="CVC" style={{ flex: 1 }} />
        </div>

        <button onClick={handlePayClick} className={styles.payButton}>
          Pay
        </button>
        <button onClick={handleBackClick} className={styles.payButton}>
          Back
        </button>
      </div>
    </div>
  );
};

export default Payment;
