import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./InsertPromptPage.module.css";
import Loading from "./Loading.jsx"; //

const InsertPromptPage = ({ sandboxProxy }) => {
  const [prompt, setPrompt] = useState("");
  const [generationCount, setGenerationCount] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsLoading(true);

    try {
      // Use relative URL assuming your backend and frontend share origin or proxy setup
      const url = `http://127.0.0.1:8000/api_router/generate-image/?prompt=${encodeURIComponent(prompt)}&num_images=${generationCount}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response data:", data);
      const { imageBase64, assessment } = data;
      const imageData = `data:image/png;base64,${imageBase64}`;

      console.log("breach:", assessment?.breach);
      if (assessment?.breach === true ) {
        const assessment_violation = assessment?.violations;
        console.log("assessment violation", assessment_violation)
        //const imageData =imageBase64;
        navigate("/bad-picture", { state: { imageData, assessment_violation, prompt } });
      } else {
        navigate("/good-picture", { state: { imageData } });
      }
    } catch (error) {
        console.error("Error generating image:", error);
        alert("Something went wrong while generating the image. Please try again.");
        setIsLoading(false);
      

    }
    finally {
    setIsLoading(false);  // Make sure to reset loading state always
    }
  };

  if (isLoading) {
    return <Loading />;
}


  return (
    <div className={styles.container}>
      <div className={styles.formBox}>
        <label className={styles.label}>Prompt</label>
        <textarea
          className={styles.textarea}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="generate Mickey Mouse..."
          rows={4}
        />

        <div className={styles.sliderField}>
          <div className={styles.sliderLabels}>
            <span>1</span>
            <input
              type="range"
              min="1"
              max="3"
              value={generationCount}
              onChange={(e) => setGenerationCount(Number(e.target.value))}
            />
            <span>3</span>
          </div>
          <label>Number of Generations</label>
        </div>

        <button className={styles.generateButton} onClick={handleGenerate}>
          Generate
        </button>
      </div>
    </div>
  );
};

export default InsertPromptPage;
