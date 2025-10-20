// import React from "react";
// import { createRoot } from "react-dom/client";
// import App from "./components/App.jsx";

// window.addEventListener("unhandledrejection", (event) => {
//   console.error("Unhandled promise rejection:", event.reason);
// });

// async function startApp() {
//   try {
//     const sdk = await import("https://new.express.adobe.com/static/add-on-sdk/sdk.js");

//     if (sdk?.default?.ready) {
//       await sdk.default.ready;
//       const { runtime } = sdk.default.instance;

//       const sandboxProxy = await runtime.apiProxy("documentSandbox");

//       const root = createRoot(document.getElementById("root"));
//       root.render(<App addOnUISdk={sdk.default} sandboxProxy={sandboxProxy} />);
//     } else {
//       throw new Error("Adobe Add-on SDK not ready");
//     }
//   } catch (err) {
//     console.error("Failed to load SDK:", err);
//   }
// }

// startApp();
// index.js - Fixed version
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App.jsx";

// Enhanced error handling for unhandled promise rejections
window.addEventListener("unhandledrejection", (event) => {
  console.error("Unhandled promise rejection:", event.reason);
  console.error("Promise that was rejected:", event.promise);
  // Prevent the default browser behavior that logs to console
  event.preventDefault();
});

// Global error handler for runtime errors
window.addEventListener("error", (event) => {
  console.error("Global error:", event.error);
  console.error("Error message:", event.message);
  console.error("File:", event.filename);
  console.error("Line:", event.lineno);
});

async function startApp() {
  try {
    console.log("Starting Adobe Express Add-on...");
    
    const sdk = await import("https://new.express.adobe.com/static/add-on-sdk/sdk.js");
    console.log("SDK imported successfully");

    if (sdk?.default?.ready) {
      console.log("Waiting for SDK to be ready...");
      await sdk.default.ready;
      console.log("SDK is ready");
      
      const { runtime } = sdk.default.instance;
      console.log("Runtime instance obtained");

      const sandboxProxy = await runtime.apiProxy("documentSandbox");
      console.log("Sandbox proxy created");

      const rootElement = document.getElementById("root");
      if (!rootElement) {
        throw new Error("Root element not found in DOM");
      }

      const root = createRoot(rootElement);
      console.log("React root created, rendering app...");
      
      root.render(<App addOnUISdk={sdk.default} sandboxProxy={sandboxProxy} />);
      console.log("App rendered successfully");
    } else {
      throw new Error("Adobe Add-on SDK not ready - SDK object or ready method missing");
    }
  } catch (err) {
    console.error("Failed to load SDK or start app:", err);
    console.error("Error stack:", err.stack);
    
    // Show user-friendly error message
    const rootElement = document.getElementById("root");
    if (rootElement) {
      rootElement.innerHTML = `
        <div style="padding: 20px; text-align: center; color: red;">
          <h3>Failed to load add-on</h3>
          <p>Error: ${err.message}</p>
          <p>Please check the console for more details.</p>
        </div>
      `;
    }
  }
}

// Start the app
startApp();