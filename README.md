🚀 Production-Ready DevOps Pipeline

📌 Project Overview

This project demonstrates the transformation of a buggy and multi-service application into a production-ready system using DevOps best practices. The application consists of multiple services that communicate through a shared queue and must be containerized, tested, secured and deployed through a fully automated pipeline.

🧩 The Application Architecture

The system is a job processing platform made up of:

- Frontend (Node.js): handles job submission and status tracking
- API (Python / FastAPI): creates jobs and exposes status endpoints
- Worker (Python): it processes jobs asynchronously
- Redis: it acts as a message broker between API and worker


🎯 Project Goals

This project focuses on simulating real DevOps responsibilities such as identifying and fixing hidden bugs in an unfamiliar codebase, containerizing a multi-service system using best practices, building a fully automated CI/CD pipeline, ensuring service reliability and health management, enforcing security and compliance checks and implementing zero-downtime deployment strategy


⚙️ Prerequisites

Before running this project, ensure you have:

- Docker
- Docker Compose
- Git
- GitHub account
- Linux/macOS (or WSL on Windows)

🛠️ Getting Started (Local Setup)

1. Clone Your Fork
git clone https://github.com/<your-username>/hng14-stage2-devops.git
cd hng14-stage2-devops

2. Create Environment Variables
cp .env.example .env

Edit .env with your configuration values.

3. Start the Full Stack
docker-compose up --build

✅ Expected Result

- All services start successfully
- Health checks pass
- No container crashes
- Frontend is accessible in browser
- Jobs can be submitted and processed successfully

🐳 Containerization Highlights

Each service is built with the following production-grade standards:

Multi-stage Docker builds (optimized image size)
Non-root users for security
HEALTHCHECK implemented for all services
No secrets baked into images
Lightweight and minimal runtime environments

🔗 Service Communication
- All services run on a private Docker network
- Redis is internal-only (not exposed externally)
- Services depend on health status, not just startup order

🔄 CI/CD Pipeline

The pipeline is implemented using GitHub Actions and runs in strict stages:

Lint → Test → Build → Security Scan → Integration Test → Deploy

🔍 Lint

Python: flake8
JavaScript: eslint
Dockerfiles: hadolint

🧪 Test

Pytest for API
Redis mocked
Minimum 3 unit tests
Coverage report generated and stored as artifact

🏗️ Build

Build all service images
Tag images with:
latest
Git commit SHA
Push to local Docker registry (within pipeline)

🔐 Security Scan

Scan images using Trivy
Pipeline fails on CRITICAL vulnerabilities
Results uploaded as SARIF

🔗 Integration Test

Full stack spins up inside runner
Job submitted via frontend
System polled until completion
Final status validated
Stack torn down cleanly


🚀 Deploy (Main Branch Only)

- Rolling update strategy implemented
- New container must pass health check before replacing old
- Timeout: 60 seconds
- Automatic rollback if deployment fails


🐞 Bug Fix Documentation

All discovered issues are documented in FIXES.md and each entry includes:

- File name
- Line number
- Description of issue
- Fix implemented


📂 Project Structure
.
├── frontend/              # Node.js frontend
├── api/                   # FastAPI backend
├── worker/                # Background worker
├── docker/                # Dockerfiles
├── nginx/                 # Reverse proxy config (if applicable)
├── docker-compose.yml     # Multi-service orchestration
├── .github/workflows/     # CI/CD pipeline
├── FIXES.md               # Bug fixes documentation
├── .env.example           # Environment variables template
└── README.md

🔐 Security Considerations

- No secrets stored in repository
- .env excluded from version control
- Images scanned for vulnerabilities
- Services run as non-root users
- Internal network isolation enforced

💼 Organizational Value

This setup delivers real organizational impact such as:

✅ Reliability: health checks and dependency management ensure system stability

✅ Faster Delivery: CI/CD automates testing and deployment

✅ Security: continuous vulnerability scanning prevents insecure releases

✅ Scalability: containerized services scale independently

✅ Maintainability: clear separation of services improves debugging and updates

📈 Conclusion

This project demonstrates how DevOps transforms a fragile system into a robust, secure and production-ready platform. 

It reflects real-world engineering expectations such as:

- Debugging unknown systems
- Automating everything
- Ensuring uptime and reliability

👤 Author

Temitope Ilori
DevOps Engineer

GitHub: https://github.com/Cybertemi
LinkedIn: https://www.linkedin.com/in/iloritemi


