# Arches Lingo

## About Lingo

### References
- [1] Contains information from the J. Paul Getty Trust, Getty Research Institute, the Art & Architecture Thesaurus, which is made available under the ODC Attribution License.

## Setup
### Note: This is a guide to set up the project for local development.

1. Download the arches-lingo repo:

    a.  If using the [Github CLI](https://cli.github.com/): `gh repo clone archesproject/arches-lingo`
    
    b.  If not using the Github CLI: `git clone https://github.com/archesproject/arches-lingo.git`

2. Download the arches package:

    a.  If using the [Github CLI](https://cli.github.com/): `gh repo clone archesproject/arches`

    b.  If not using the Github CLI: `git clone https://github.com/archesproject/arches.git`

3. Create a virtual environment outside of both repositories: 
    ```
    python3 -m venv ENV
    ```

4. Activate the virtual enviroment in your terminal:
    ```
    source ENV/bin/activate
    ```

5. Navigate to the arches-rdm package, and install it into the virtual environment:
    ```
    cd arches
    pip install -e .
    ```

6. Navigate to the arches_lingo, and install the python requirements:
    ```
    cd ../arches-lingo
    pip install -r arches_lingo/install/requirements.txt
    ```

7. Run the Django server:
    ```
    python manage.py runserver
    ```

8. **OPEN A NEW TERMINAL WINDOW**, the following step will take place in a new terminal window while the python server is running.

9. Ensure this new terminal window has the virtual environment activated.
    ```
    source ENV/bin/activate
    ```

10. Navigate to your project then install the frontend dependencies.
    ```
    cd arches-lingo/
    npm install
    ```

11. Once the dependencies have been installed, generate the static asset bundle:

    a. If you're planning on editing HTML/CSS/JavaScript files, run `npm start`. This will start a development server that will automatically detect changes to static assets and rebuild the bundle.

    b. If you're not planning on editing HTML/CSS/JavaScript files, run `npm run build_development`

12. If you ran `npm start` in the previous step, you will need to open a new terminal window and activate the virtual environment in the new terminal window. If you ran `npm run build_development` then you can skip this step.

13. Navigate to the arches_lingo top-level directory, and install the ontologies, branches, and resource models from the arches-rdm package.
    ```
    python manage.py setup_db
    python manage.py packages -o load_package -s arches_lingo/pkg --yes -db
    ```

14. In the terminal window that is running the Django server, halt the server and restart it.
    ```
    (ctrl+c to halt the server)
    python manage.py runserver
    ```

## Committing changes

NOTE: Changes are commited to the arches-rdm repository. 

1. Navigate to the repository
    ```
    cd arches-lingo
    ```

2. Cut a new git branch
    ```
    git checkout origin/master -b my-descriptive-branch-name
    ```

3. If updating models or branches

    1. Manually export the model or branch from the project

    2. Manually move the exported model or branch into one of the subdirectories in the `arches-lingo/arches_lingo/pkg/graphs` directory.

4. Add your changes to the current git commit
    ```
    git status
    git add -- path/to/file path/to/second/file
    git commit -m "Descriptive commit message"
    ```

5. Update the remote repository with your commits:
    ```
    git push origin HEAD
    ```

6. Navigate to https://github.com/archesproject/arches-lingo/pulls to see and commit the pull request
