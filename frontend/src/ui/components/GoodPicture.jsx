import React, { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./GoodPicture.module.css";


// Import the Adobe SDK directly (same as your working example)
import AddOnSdk from "https://new.express.adobe.com/static/add-on-sdk/sdk.js";

// Helper to convert base64 data URI to Blob (same as your working example)
async function getBlob(url) {
  const response = await fetch(url);
  return response.blob();
}

// Reusable function to enable drag and drop (same as your working example)
function enableDragToDocument(imageElement) {
  AddOnSdk.app.enableDragToDocument(imageElement, {
    previewCallback: (element) => {
      return new URL(element.src); // Preview the image being dragged
    },
    completionCallback: async (element) => {
      const blob = await getBlob(element.src); // Get the blob when dropped
      return [{ blob }];
    }
  });
}

const GoodPicture = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { imageData } = location.state || {};
  const imageRef = useRef(null);
  const [sdkReady, setSdkReady] = useState(false);

  useEffect(() => {
    // Wait for Adobe SDK to load and be ready (same pattern as your working example)
    AddOnSdk.ready.then(async () => {
      setSdkReady(true);
    });
  }, []);

  useEffect(() => {
    // Enable drag-to-document when SDK is ready and image ref is available
    if (sdkReady && imageRef.current) {
      enableDragToDocument(imageRef.current);
    }
  }, [sdkReady, imageData]); // Added imageData as dependency to re-enable when image changes

  const handleBack = () => {
    navigate(-1);
  };

  if (!imageData) {
    return <div>No image available. Please generate one first.</div>;
  }

  return (
        <div className={styles.container}>
        <h2 className={styles.heading}>
          Drag and drop your generation results to your canvas
        </h2>
        <div className={styles.imageWrapper}>
          <img
            src={imageData}
            alt="Generated"
            className={styles.image}
            ref={imageRef}
            draggable="true"
          />
        </div>
        <button className={styles.backButton} onClick={handleBack}>
          Back
        </button>
      </div>
    );
};


export default GoodPicture;