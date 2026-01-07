# GitHub Setup Guide

Your local repository has been initialized and all files have been committed. Follow these steps to push to GitHub:

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `intelligent-workflow-builder` (or your preferred name)
   - **Description**: "No-Code/Low-Code web application for building intelligent AI workflows"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your terminal:

### Option A: If you haven't set up the remote yet

```bash
cd D:\assignmnet
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with the repository name you created

### Option B: If you prefer SSH (if you have SSH keys set up)

```bash
cd D:\assignmnet
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

After pushing, refresh your GitHub repository page. You should see all your files there!

## Quick Commands Reference

```bash
# Check current status
git status

# View remote repositories
git remote -v

# Push to GitHub
git push origin main

# If you need to update the remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Important Notes

- **Never commit `.env` files** - They contain sensitive API keys
- The `.gitignore` file is already configured to exclude:
  - `.env` files
  - `node_modules/`
  - `__pycache__/`
  - Database files
  - Upload directories
  - And other sensitive/generated files

## Next Steps After Pushing

1. Add a repository description on GitHub
2. Consider adding topics/tags: `workflow-builder`, `react`, `fastapi`, `ai`, `llm`, `no-code`
3. Update the README if needed with your specific repository URL
4. Consider adding a LICENSE file if you want to open source it

## Troubleshooting

### If you get authentication errors:
- Use a Personal Access Token instead of password
- Or set up SSH keys for easier authentication

### If the branch name is different:
- Your default branch might be `master` instead of `main`
- Use: `git push -u origin master` (or whatever your branch name is)

### To check your current branch:
```bash
git branch
```

