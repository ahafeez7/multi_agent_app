"# multi_agent_healthcare_app" 
# git init
# git add README.md
# git commit -m "Initial commit"
# git branch -M main
# git remote add origin git@github.com:ahafeez7/multi_agent_healthcare_app.git
# git push -u origin main
#########################To remove .streamlit/secrets.toml if committed accidently#########################
# git rm --cached app/.streamlit/secrets.toml
# git commit -m "Remove secrets.toml from version control"
# git push origin main
# for future add this line to your .gitignore
# app/.streamlit/secrets.toml
# Optional (Not recommended if multiple users using this repo): to remove secrets from entire repo history -- make sure it's not in old commits
# git filter-repo --path app/.streamlit/secrets.toml --invert-paths
# git push --force