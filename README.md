# Ark Tracker BACKEND

## Overview

Backend project for Ark Tracker a to-do style app for the game of Lost Ark. Add/delete characters and track daily/weekly tasks for each character. All tasks require user input.

### Technologies

- Python version 3.9.7
- Flask version 2.0.3
- Flask-Cors version 3.0.10
- Mariadb version 1.0.10

### Intructions

- Clone or download repository

- import sql file into database

- setup a virtual enviroment

- run 'python3.9 api.py testing' to run the API **NOTE** command can change depending on OS used, in my case I am using WSL

It is reccommended to have PM2 for deployment to ensure your backend API is always up. It also comes with great error logging if your app is having issues.
You will also need to ensure you have setup Apache or whatever you use to direct the requests to the backend properly

## License

Ark Tracker is available under the MIT license. See the [HERE](LICENSE.MIT) for more info.
