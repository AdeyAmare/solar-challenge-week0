# KAIM-Week-0: Solar Challenge

# Task 1: Git & Environment Setup Overview

This repository was initialized to fulfill the environment setup and version control requirements for the KIAM-Week-0 challenge.

# Key Deliverables

- Repository Initialization: Created and cloned the solar-challenge-week0 repository.

- Virtual Environment: Set up a Python virtual environment (venv).

- Version Control: Implemented .gitignore, requirements.txt, and committed changes on a dedicated branch (setup-task).

- Continuous Integration (CI): Added a GitHub Actions workflow (.github/workflows/ci.yml) to ensure dependency installation is working.

# Reproducing the Environment

1. Clone the project from GitHub (replace <your-username> with your actual GitHub username):
   
```
git clone https://github.com/<your-username>/solar-challenge-week0.git
cd solar-challenge-week0
```

2. Create and Activate the Virtual Environment
   
- Create the venv:
```
python -m venv .venv
```

- Activate the venv
```
.venv\Scripts\activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. CI Workflow

A GitHub Actions workflow is set up in .github/workflows/ci.yml to automatically run ```pip install -r requirements.txt``` and verify the Python version on every push and pull request.

