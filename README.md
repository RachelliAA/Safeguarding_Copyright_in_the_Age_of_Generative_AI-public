**Safeguarding Copyright in the Age of Generative AI
**
Our project is an intelligent agent-based framework that helps organizations and creators generate AI content responsibly. It automatically checks outputs from generative models (like DALL·E, Stable Diffusion, or Midjourney) against intellectual property (IP) policies and performs real-time copyright compliance assessments.
When potential infringements are detected, the system can:
Suggest licensing options, or
Perform prompt optimization - automatically rewriting prompts to maintain creativity while avoiding copyright risks.

System Components:
  1. Policy Agent
Parses IP policies written in natural language.
Converts them into enforceable JSON-based rules.
Logs all policy decisions for traceability.

  2. Assessment Agent
Evaluates generated content using:
CLIP-based similarity detection
Approximate Nearest Neighbor (ANN) image matching
Risk ranking and structured reporting
Returns standardized compliance results in JSON format.

  3. Prompt Optimization Agent
Iteratively refines prompts to minimize similarity with protected works.
Balances compliance with creative intent.

  4. Frontend Interface (Node.js + React)
Built with React for interactive, real-time monitoring of generation results.
Node.js backend connects to the FastAPI layer via REST.

Displays:
Policy evaluation results
Risk levels and similarity visualizations
Prompt optimization suggestions

Tech Stack:
Python - core logic & AI orchestration
FastAPI - backend API layer
Pydantic - structured validation
CLIP + ANN Search - image similarity
Image-to-Text (I2NL) - semantic captioning
RAG Integration - live IP policy retrieval
Node.js + React - user interface and visualization
