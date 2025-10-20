
import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './SimilarImages.model.css'; // Adjust the path as necessary

// Import the Adobe SDK directly
import AddOnSdk from "https://new.express.adobe.com/static/add-on-sdk/sdk.js";

// Helper function to get blob (same as your working example)
async function getBlob(url) {
  const response = await fetch(url);
  return response.blob();
}

// Reusable function to enable drag and drop
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

const SimilarImages = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { imageData, prompt } = location.state || {};
  const [sdkReady, setSdkReady] = useState(false);
  
  // Create refs for each image
  const image1Ref = useRef(null);
  //const image2Ref = useRef(null);

  useEffect(() => {
    // Wait for Adobe SDK to load and be ready
    AddOnSdk.ready.then(async () => {
      setSdkReady(true);
    });
  }, []);

  useEffect(() => {
    // Enable drag-to-document when SDK is ready and image refs are available
    if (sdkReady) {
      if (image1Ref.current) {
        enableDragToDocument(image1Ref.current);
      }
      // if (image2Ref.current) {
      //   enableDragToDocument(image2Ref.current);
      // }
    }
  }, [sdkReady, imageData]); // Re-enable when SDK is ready or image changes

  if (!imageData) {
    return <p>No image available.</p>;
  }

  return (
    <div className="container">
      <p className="description">
        Check out these similar images we found for you, drag and drop any of them to your canvas
      </p>
      <div className="images-wrapper">
        <div className="image-box">
          <img 
            ref={image1Ref}
            src={imageData} 
            alt="Similar Image 1" 
            className="similar-image"
            draggable="true"
          />
        </div>
        {/* <div className="image-box">
          <img 
            ref={image2Ref}
            src={imageData} 
            alt="Similar Image 2" 
            className="similar-image"
            draggable="true"
          />
        </div> */}
      </div>
      <button className="backButton" onClick={() => navigate(-1)}>Back</button>
    </div>
  );

};

export default SimilarImages;