Deploying a Python Application with Firebase Free Hosting This guide outlines the steps to deploy a Python application using Firebase's free hosting tier.

Upgrade to the Blaze Plan and Create a Project:

Log in to the Firebase console.

To use Firebase Hosting services, you must upgrade your project to the "Blaze" (Pay-as-you-go) plan. This plan includes a generous free monthly quota, and you will only be charged for usage that exceeds it.

Create a new Firebase project (e.g., linebot).

Install Firebase CLI:

Install the Firebase Command Line Interface (CLI) globally using npm (Node Package Manager).

Bash

npm install -g firebase-tools

Set Up Your Project Directory:

Create a main directory for your project (e.g., firebase-flask).

Inside this directory, create a subdirectory named functions. Your Python code will be placed here.

Log In to Firebase:

Authenticate with your Firebase account through the CLI.

Bash

firebase login Initialize Your Firebase Project:

Navigate to your main project directory (firebase-flask) and run the initialization command.

Bash

firebase init

Configure Firebase Features:

When prompted, use the arrow keys and spacebar to select both Hosting and Functions. Choose the existing Firebase project you created earlier (e.g., linebot). Firebase will ask for the location of your public files; you can leave this as the default (public). However, the final deployment will be served from the functions directory.

Configure Functions and Hosting Rewrites:

Select Python as the language for your Cloud Functions. When asked if you want to set up rewrites for all URLs to /index.html, select No. Choosing "Yes" will cause all incoming requests to be incorrectly routed to a static index.html file instead of your Python function.

Modify firebase.json:

Open the generated firebase.json file. Ensure the runtime for your function is set to your desired Python version (e.g., python311). Verify or add the rewrites configuration to direct all hosting requests to your function. It should look like this:

JSON

{ "hosting": { // ... other settings "rewrites": [ { "source": "**", "function": "yourFunctionName" } ] }, "functions": { "runtime": "python311" } } (Note: Replace yourFunctionName with the name of the function defined in your Python code.)

Deploy Your Application:

Once your Python code is ready in the functions directory, deploy it to Firebase.

Bash

firebase deploy Local Testing and Debugging (Optional):

To test your application locally before deploying, use the Firebase emulator suite.

Bash

firebase serve For testing external webhooks (like from a messaging app), you can use a tool like ngrok to create a secure public URL that forwards requests to your local machine. You can use curl to send POST or GET request to your application, curl -X POST -H "Content-Type: application/json"
-d '{"Status": "Succesfully"}'
https://your-project-id.web.app/some/path

curl https://your-project-id.web.app/some/path?status=Succesfully

Verify and Test:

After deployment, visit your Firebase Hosting URL to test the live application and ensure all functions are working as expected.

Note: Make sure you are running under venv. You have to deploy vene at functions folder, python -m venv venv source venv/bin/activate pip install -r requirements.txt
