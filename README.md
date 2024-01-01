# PDF Image and Text Extract

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/vishalnagda1/gotech-task/blob/main/LICENSE)

PDF Image and Text Extract is a Python-Django project and uses the PostgreSQL database to store the data.

**PDF Image and Text Extract project following APIs**

- SignUp
- SignIn
- File upload
- File list (list all the files which are uploaded by the user)
- Rename File
- Delete File
- Download File
- Extract File Data
- SignOut



## Requirements

##### **Prerequisites**

You should have at least a basic understanding of fundamental programming concepts and some experience with introductory [`Python`](https://www.python.org/). And the knowledge of [`Django` framework](https://www.djangoproject.com/) is an advantage.

##### **Install**

Lastly, make sure you have the following installed.

- Latest version of [Python](https://www.python.org/)
- Latest version of [PostgreSQL](https://www.postgresql.org/)
- Latest version of [git](https://git-scm.com/) (**This is optional. It requires only if you choose to clone project**)



### Getting Started

1. Either you can **clone** or **download** repository from GitHub.

   - Clone with HTTPS *(required [git](https://git-scm.com/) installed in your system)*

     ```shell
     git clone https://github.com/vishalnagda1/gotech-task.git
     ```

   - Clone with SSH *(required [git](https://git-scm.com/) installed in your system)*

     ```sh
     git clone git@github.com:vishalnagda1/gotech-task.git
     ```

   - [Download Zip](https://github.com/vishalnagda1/gotech-task/archive/main.zip)

2. Navigate to project directory in the terminal or command prompt.

   ```shell
   cd gotech-task
   ```

3. Create a virtual environment

   ```shell
   python3 -m venv .venv
   ```

4. Activate the virtual environment

   ```shell
   source .venv/bin/activate
   ```

5. Install project dependencies

   ```shell
   pip install -r requirements.txt
   ```

6. Run the project server

   - Run **local system** server

     ```shell
     python manage.py runserver 0.0.0.0:8000
     ```
     **NOTE**: You need the adjust your `DB Host` config in your project settings file.

        OR

   - If you want to use [docker](https://www.docker.com/)

     ```shell
     docker-compose up
     ```

     **NOTE**: If you want to use db-admin web panel, then you can uncomment db-admin service in docker-compose.yml file.

   - If you want to make a build of your app

     ```shell
     docker-compose build
     ```
       

7. Project server is running at: [http://0.0.0.0:8000](http://localhost:8000)



#### APIs:

1. SignUp API

   - Endpoint - `/pdf/signup/`

   - HTTP Method - POST

   - Payload

     ```json
     {
         "username": "test",
         "password": "test"
     }
     ```

2. SignIn API

   - Endpoint - `/pdf/signin/`

   - HTTP Method - POST

   - Payload

     ```json
     {
         "username": "test",
         "password": "test"
     }
     ```

3. File Upload API

   - Endpoint - `/pdf/upload/`

   - HTTP Method - POST

   - Payload: `form-data`

     ```
     file: <file/path.pdf>
     ```

4. File list API

   - Endpoint - `/pdf/list/`

   - HTTP Method - GET

5. Rename File API

   - Endpoint - `/pdf/rename/<int:file_id>/`
   - Example - `/pdf/rename/1/`

   - HTTP Method - POST

   - Payload

     ```json
     {
         "new_name": "test.pdf"
     }
     ```

6. Delete File API

   - Endpoint - `/pdf/delete/<int:file_id>/`
   - Example - `/pdf/delete/1/`

   - HTTP Method - DELETE

7. Download File API

   - Endpoint - `/pdf/download/<int:file_id>/`
   - Example - `/pdf/download/1/`

   - HTTP Method - GET

   - Payload

     ```json
     {
         "new_name": "test.pdf"
     }
     ```

8. Extract File Data API

   - Endpoint - `/pdf/extract/<int:file_id>/`
   - Example - `/pdf/extract/1/`

   - HTTP Method - POST

   - Payload

     ```json
     {
         "force_extraction": false
     }
     ```

9. SignOut API

   - Endpoint - `/pdf/signout/`

   - HTTP Method - GET




#### Contributing

1. Fork it ( https://github.com/vishalnagda1/gotech-task/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new pull request.
