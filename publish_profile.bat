@echo off
setlocal
cd /d "%~dp0"
set "REPO=LonzilFox/LonzilFox"
where git >nul 2>&1 || (echo ERROR: Git not found.& pause & exit /b 1)
where gh >nul 2>&1 || (echo ERROR: GitHub CLI not found.& pause & exit /b 1)
gh auth status >nul 2>&1 || (echo ERROR: Run gh auth login first.& pause & exit /b 1)
if not exist .git (git init || exit /b 1)
git branch -M main || exit /b 1
git add . || exit /b 1
git diff --cached --quiet
if errorlevel 1 (git commit -m "Update LonzilFox profile README" || (echo ERROR: Git commit failed.& pause & exit /b 1))
gh repo view "%REPO%" >nul 2>&1
if errorlevel 1 (
  gh repo create "%REPO%" --public --source "." --remote origin || (echo ERROR: Could not create repository.& pause & exit /b 1)
)
git remote get-url origin >nul 2>&1
if errorlevel 1 git remote add origin "https://github.com/%REPO%.git"
git push -u origin main
if errorlevel 1 (echo ERROR: Push rejected. Existing history not overwritten.& pause & exit /b 1)
echo Profile: https://github.com/LonzilFox
pause
