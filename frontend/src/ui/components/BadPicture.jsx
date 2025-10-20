import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './BadPicture.module.css';
import Loading from './Loading.jsx';

const warning = require('../assets/warning.png');


const IPWarning = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { imageData, assessment_violation, prompt } = location.state || {};

  const [loading, setLoading] = useState(false);

  const handleCreateSimilar = async () => {
    if (!imageData || !prompt ) 
    { 
      console.error("Image data or prompt is missing");
      return;
    }

    setLoading(true);

    try {
      console.log( prompt, assessment_violation,imageData);

      const response = await fetch("http://127.0.0.1:8000/api_router/generate-image-with-iteration", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          imageData: imageData,
          prompt: prompt,             
          breach_reason: assessment_violation,  
        }),
      });

      console.log("response:", response)
      if (!response.ok)
         throw new Error('Image generation failed');

      const data = await response.json();
      console.log("Generated similar image data:", data);

      const newImageBase64 = `data:image/png;base64,${data.imageBase64}`;

      navigate("/similar-Images", {
        state: {
          imageData: newImageBase64,
          finalPrompt: data.finalPrompt,
        },
      });

    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (!imageData) {
    return <div>No image available. Please generate one first.</div>;
  }

  if (loading) {
    return  <Loading />;
  }

  return (
    <div className={styles.container}>

     <div className={styles.warning}>
        <img src={warning} alt="Warning" className={styles.warningIcon} />
        <div className={styles.warningText}>
          <span>The generated image is infringing on IP rights</span>
        </div>
     </div>


      <div className={styles.imageWrapper}>
        <img src={imageData} alt="Flagged content" className={styles.image} />
      </div>

      <div className={styles.actions}>
        <div>
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                navigate('/payment', { state: { imageData } });
              }}
              className={styles.action}
            >
              I want to license for $1
            </a>
          <p className={styles.actionText}>
            You’ll be redirected to a secure payment page and gain risk-free usage rights
          </p>
        </div>

        <div>
          <a href="#" onClick={(e) => { e.preventDefault(); handleCreateSimilar(); }} className={styles.action}>
            Help me create a similar image
          </a> 

          <p className={styles.actionText}>
            No worries — we’ll optimize your prompt to generate a similar, risk-free image.
            <br />
            <small className={styles.actionSubText} >Extra tokens may be used</small>
          </p>
        </div>
      </div>

      <button className={styles.backButton} onClick={() => navigate(-1)}>
        Back
      </button>
    </div>
  );
};

export default IPWarning;
