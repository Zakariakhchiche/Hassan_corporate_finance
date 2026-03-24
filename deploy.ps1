# Script de déploiement Vercel
# 1. Assurez-vous d'avoir installé Vercel CLI : npm install -g vercel
# 2. Connectez-vous à Vercel : vercel login
# 3. Exécutez ce script : .\deploy.ps1

Write-Host "🚀 Déploiement de Hassan Corporate RAG sur Vercel..." -ForegroundColor Green

# Déploiement du frontend Next.js
Write-Host "📦 Déploiement du frontend..." -ForegroundColor Yellow
npx vercel deploy --prod --yes

Write-Host "✅ Déploiement terminé !" -ForegroundColor Green
