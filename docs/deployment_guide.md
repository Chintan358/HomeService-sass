# Deployment Guide – Home Services Booking SaaS

This guide explains how to get the **frontend** (React + Vite) onto **Vercel**, the **backend** (FastAPI) onto **Render**, and how the CI/CD pipeline in GitHub Actions ties everything together.

---

## Prerequisites
- GitHub account with the repository containing the code.
- Vercel account (https://vercel.com) – for the frontend.
- Render account (https://render.com) – for the backend.
- Docker Hub account (optional, used by Render to pull the image).
- Razorpay test credentials, Cloudinary URL, and a secret JWT key.

---

## 1️⃣ Set up GitHub Secrets
Navigate to **Repository → Settings → Secrets → Actions** and add the following secrets (values come from your `.env` or the services you’ll use):

| Secret | Description |
|--------|-------------|
| `VERCEL_TOKEN` | Vercel personal token (`vercel token`). |
| `DOCKERHUB_USERNAME` | Your Docker Hub username. |
| `DOCKERHUB_TOKEN` | Docker Hub access token (or password). |
| `RENDER_DEPLOY_HOOK_URL` | Deploy hook URL from Render (Web Service → Deploy Hooks → New Hook). |
| `SECRET_KEY` | Random string used for JWT signing. |
| `RAZORPAY_KEY_ID` | Razorpay test key ID. |
| `RAZORPAY_KEY_SECRET` | Razorpay test secret. |
| `CLOUDINARY_URL` | Cloudinary connection string (e.g., `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`). |
| `DATABASE_URL` | Render‑provided MySQL connection string (or `sqlite:///./test.db` for local dev). |

---

## 2️⃣ Frontend – Vercel
1. In the Vercel dashboard click **“New Project”** → **Import Git Repository** → select this GitHub repo.
2. Choose **Framework Preset → Other** (Vite builds fine with the defaults).
3. Set **Build Command** to `npm run build`.
4. Set **Output Directory** to `dist`.
5. Click **Deploy**.
6. Vercel will provide a preview URL (`<project>.vercel.app`). Pushes to `main` automatically trigger a new deployment.

---

## 3️⃣ Backend – Render (Docker)
1. In Render, click **“New Web Service”** → **Docker**.
2. Connect the same GitHub repository.
3. Render will read `backend/render.yaml` automatically – you do not need to edit anything else.
4. Ensure the **Deploy Hook** URL matches the secret `RENDER_DEPLOY_HOOK_URL`.
5. Add any additional environment variables that are not in `render.yaml` via the Render UI.
6. Click **Create Web Service**. Render builds the Docker image using `backend/Dockerfile` and starts the service.
7. Health‑check endpoint: `GET /me` (returns 200 if the service is alive).

---

## 4️⃣ Docker Hub (optional)
If you prefer Render to pull a pre‑built image rather than building on each push:
```bash
cd backend
docker build -t yourdockerhubuser/home-services-backend:latest .
docker push yourdockerhubuser/home-services-backend:latest
```
Update `render.yaml` to reference the image name instead of a Dockerfile path.

---

## 5️⃣ CI/CD – GitHub Actions (`.github/workflows/deploy.yml`)
The workflow runs on every push to `main`:
1. **Test** – Lint, format, and run the full pytest suite.
2. **Frontend Build** – `npm ci && npm run build`, then deploy to Vercel using the `vercel` CLI.
3. **Backend Build** – Build the Docker image, push it to Docker Hub, then trigger Render via the Deploy Hook.
4. If any step fails, the workflow aborts and no deployment occurs.

You can view the live status under the **Actions** tab of the repository.

---

## 6️⃣ Verify Deployments
- **Frontend**: Open `https://<your‑project>.vercel.app` – you should see the landing page and be able to register / log in.
- **Backend**: Open `https://<your‑service>.onrender.com/docs` – Swagger UI with all endpoints.
- **Health**: `GET https://<your‑service>.onrender.com/me` returns `{"id":..., "email":..., "role":...}` when a valid JWT is supplied.

---

## 7️⃣ Post‑Deployment Checklist
- [ ] Enable **HTTPS** (both Vercel and Render enforce it by default).
- [ ] Restrict CORS origins to your production domain (instead of `*`).
- [ ] Rotate `SECRET_KEY` and other credentials periodically.
- [ ] Set up monitoring/alerting (Render logs, Vercel analytics, optional Sentry). 
- [ ] Review the **Security Checklist** (rate limiting, security headers, OWASP). 

---

**You’re all set!** Every push to `main` will automatically lint, test, build, and deploy the app. Use the GitHub repo URL as the final submission link.
