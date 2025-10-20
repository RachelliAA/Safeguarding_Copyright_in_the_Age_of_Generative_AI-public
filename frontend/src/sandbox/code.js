import addOnSandboxSdk from "add-on-sdk-document-sandbox";
import { editor } from "express-document-sdk";

// Get the document sandbox runtime.
const { runtime } = addOnSandboxSdk.instance;

function start() {
    // APIs to be exposed to the UI runtime
    // i.e., to the `index.html` file of this add-on.
    const sandboxApi = {
                addImageToDocument: async (imageBlob) => {
            console.log("addImageToDocument called with blob:", imageBlob);
            try {
                // Create an image using the editor's SDK
                const image = editor.createImage();
                
                // Use URL.createObjectURL for the image blob (more efficient for most cases)
                const imageUrl = URL.createObjectURL(imageBlob);
                image.source = imageUrl;
                image.width = 300;
                image.height = 200;
                image.translation = { x: 50, y: 50 };

                // Append the image to the editor's document
                editor.context.insertionParent.children.append(image);

                console.log("Image added successfully.");
            } catch (error) {
                console.error("Error in addImageToDocument:", error);
            }
        },
    };

    console.log("Exposing sandbox API:", sandboxApi);
    runtime.exposeApi(sandboxApi);
}

start();
