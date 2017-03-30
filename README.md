[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

# BlogIt! - Free Blogging Platform

## Table of Contents
- [Background](#background)
- [Author](#author)
- [How to Use](#how-to-use)
- [Source Files](#source-files)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Background
This code launches a multi user blog platform that supports following features:
  - Users can register themselves and login as well as logout.
  - Users can like other users posts (but not their own posts), and see number of likes on a post.
  - Users can comment on posts, edit/delete their own comments.
  - Users can edit and delete their own posts.
  - Users can view all of their own posts with one click.
  
View live version of this app deployed on GCloud here: https://blogit-app.appspot.com/

## Author
[Sejal Parikh](https://in.linkedin.com/in/sejalparikh)

## How to Use
1. Download all the files in the same folder.
2. [Install Google Cloud SDK](https://cloud.google.com/sdk/downloads) and configure your project on the [Gcloud console](https://console.cloud.google.com/?_ga=1.161349432.42502844.1490027497).
3. Run Gcloud init, and select your account and application.
4. Run dev_appserver.py . --port &lt;port-number&gt;
5. Open http://localhost:&lt;port-number&gt;

## Source Files
blog.py - Contains all the blog handlers
main.py - contains classes and functions related to the posts and comments
secure.py - Contains all security related functions
database.py - Contains all database model definitions and related methods
base.py - Contains the basic handler that is inherited by other handlers
auth.py - Contains functions related to authorizations, such as registration, login, logout, and so on.
/templates - Holds all the html templates
/static/css - holds the common css file for the app

## License
[GNU General Public License v3](../LICENSE)
