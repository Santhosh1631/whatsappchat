# Deployment Runbook

This project is prepared for split deployment:

- Frontend on Vercel or Netlify
- Backend + Postgres on Render

## Files already prepared

- render.yaml (Render Blueprint)
- vercel.json (Vercel static build config)
- netlify.toml (Netlify build config)
- frontend/.env.example
- backend/.env.example

## 1) Render backend deployment

1. In Render dashboard click New -> Blueprint.
2. Select this GitHub repository.
3. Render reads render.yaml and creates:
   - Web service: chat-importer-api
   - Postgres: chat-importer-db
4. Open web service environment variables and set:
   - FRONTEND_ORIGIN = your frontend public URL
5. Deploy and wait for green status.

Expected backend URL format:
https://<service-name>.onrender.com

Health check sample:
https://<service-name>.onrender.com/api/messages?limit=1

## 2) Vercel frontend deployment

1. In Vercel click Add New -> Project.
2. Import this GitHub repository.
3. In project settings use:
   - Root Directory: frontend
4. Add environment variable:
   - VITE_API_BASE_URL = https://<service-name>.onrender.com/api
5. Deploy.

## 3) Netlify frontend deployment (alternative)

1. In Netlify click Add new site -> Import an existing project.
2. Select this repository.
3. netlify.toml is auto-detected.
4. Add environment variable:
   - VITE_API_BASE_URL = https://<service-name>.onrender.com/api
5. Deploy.

## 4) Final CORS check

If frontend cannot call backend, re-check backend env on Render:

- FRONTEND_ORIGIN must match exact frontend domain.

Examples:
- https://my-chat-app.vercel.app
- https://my-chat-app.netlify.app

## Why I cannot complete the final publish automatically

This terminal does not have deployment credentials:
- VERCEL_TOKEN not set
- NETLIFY_AUTH_TOKEN not set

If you provide one token, deployment can be executed from CLI in one command.
