<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1TzwYWlYSF-4N66cs6t6h0JqApUC4k9PN

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`


ATI_VIODETECT/                   # project name
├── .vite/
├── backend/
│   ├── backend_structure.md     # this files will describes detailed the structure of the backend part
├── frontend/                     
│   ├── components/
│           ├── CameraFeed.tsx
│           ├── CameraSetup.tsx
│           ├── Header.tsx
│           ├── icons.tsx
│           ├── JsonViewer.tsx
│           ├── VideoUploader.tsx
│   ├── node_modules/
│   ├── .env.local
│   ├── .gitignore
│   ├── App.tsx
│   ├── index.html
│   ├── index.tsx
│   ├── metadata.json
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   ├── tsconfig.json
│   ├── types.ts
│   ├── vite.config.ts
├── cmd_docker_run.txt              # cmd how to run the project
├── cmd_local_run.txt              # cmd how to run the project