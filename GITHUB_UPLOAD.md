# Upload this project to GitHub

Suggested repository name: `oral-cancer-research-dashboard`

Suggested description: `Streamlit dashboard comparing four oral cancer classification models with leakage-aware preprocessing and out-of-fold evaluation.`

## Git command-line workflow

1. Create an empty repository in your GitHub account. Start private while dataset provenance and group-project ownership are being documented. Do not initialize another README, license or .gitignore there; these project files are already prepared.
2. Extract this ZIP and open Anaconda Prompt in the folder containing app.py, README.md and .gitignore.
3. Run:

```bat
git init
git add .
git status
git commit -m "Add oral cancer research dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/oral-cancer-research-dashboard.git
git push -u origin main
```

Replace YOUR_USERNAME with your account name. Authenticate through the Git credential prompt or GitHub CLI; do not put tokens in files or commands. If Git requests an author identity, configure your own name and email before committing.

Before committing, `git status` should NOT show `.env`, `.streamlit/secrets.toml`, local environments or the source CSV. To check the CSV ignore rule:

```bat
git check-ignore data/oral_cancer_prediction_dataset.csv
```

If you use an already-initialized repository, do not blindly repeat remote setup; inspect `git status` and `git remote -v` first.

## If Git is not installed

Create the repository in GitHub's website and use its file upload option. Upload the extracted project contents, not the ZIP file. Include `.gitignore`, `.gitattributes` and `.streamlit/config.toml`; Windows may hide some files. GitHub Desktop is another option.

## Local dataset

Copy the original CSV from your existing dashboard's data folder to this project's data folder to run locally. Git ignores it. The upload bundle contains genuine saved model results and figures, not a replacement dataset.

Creating a GitHub repository does not deploy the Streamlit app. This project has not been uploaded or published on your behalf.
