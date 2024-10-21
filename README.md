# StamiChat
Just a chat server I made in Python. It's quite easy to run, designed to work on localhost, but you could also make it work on Replit.

# INFORMATION
The code contains a list of banned words, including slurs, and I plan to add more. This list prevents users from using slurs in their messages or usernames. Feel free to add or remove words as you see fit.

# Deployment
[![Deploy on Render](https://render.com/deploy-to-render/button.svg)](https://dashboard.render.com/deploy?repo=github.com/Adamdoesdumbcode/StamiChat)
## How to deploy in Render
### Setup Instructions
1. Deploy the app using the Render button.
2. After deployment, go to your Render dashboard.
3. Under the "Environment" section, set a new environment variable:
   - **Key:** `SECRET`
   - **Value:** Your own secret key (e.g., `supersecretkey`).
