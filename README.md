# SPR 2024 CSCI4970-Capstone: Group 3: Peter Kiewit Institute Room Assignment and Scheduling Application

## ABOUT:

- [Technical Report (PDF)](https://github.com/TrevorAhlers/CSCI4970-Capsoft-Solutions-Project/blob/main/Documentation/Final%20Project%20Report%20-%20Group%203%20Capsoft%20Solutions%20-%20PKI%20Scheduler.pdf)
- [Live Demo Video](https://github.com/TrevorAhlers/CSCI4970-Capsoft-Solutions-Project/blob/main/Documentation/demo-video.mp4)

This web application is being developed to reduce the workload of the Classroom Coordinator responsible for assigning courses to rooms in the Peter Kiewit Institute (PKI) building at the University of Nebraska at Omaha.

Each semester, the Classroom Coordinator receives a CSV file containing all course sections that need room assignments in PKI. Difficulties arise when conflicts occur, and managing both scheduled and emergent conflicts has been shown to contribute to the high turnover in this role. We aim to automate as much of this process as possible and reduce the mental load on the user who utilizes our application to produce a finalized output CSV that is either conflict-free or allows conflicts to be ignored.

## RELEASE NOTES MILESTONE 5 (v1.0.0)

The final development release is completed!

Our project is fully implemented on Amazon Web Services using Elastic Beanstalk which deploys EC2 servers by demand, and the Relational Database is using AWS RDS running on an EC2 server that is not managed by Elastic Beanstalk and therefore never destroyed. The frontend is hosted on an S3 Bucket. Our domain name was updated to capsoftsolutions.com using AWS Route 53. We are using http protocol due to some delays getting certificate approval from Amazon to use https.

Our site features a consumer-ready visual design with overhauls to the theme and improvements to the resolution scaling. We've added UNO logos so users know they are in the right place. We've incorporated registered usernames to be displayed on the homepage of the web app instead of the previously persistent "Guest User". We now have a functional collapse button to hide the conflict manager and give more space to the central component, as needed. We've included a button to download a "Change Log" to clearly show in plain-text what classes were updated, and what was changed so our user can submit this directly to registrar due to the read-only access for the actual input CSV. We have input validation in place for invalid field completiton, invalid file selection, and failed login attempts.

Our Upload View component now features some exciting enhancements to improve practicality from a use-case perspective, and future-proofing the relevance of the assignment logic. Users can choose to turn off auto-assignment if they wanted to generate a change report by making some manual adjustments. This means our program can always be the solution for a Classroom Coordinator no matter what their needs are, and we are not forcing changes on the user if auto-assignment is not needed. Users can specifically choose which assignment strategies they want to use if they do have auto-assignment enabled. They choose between Historical, Historical by Department, and Predictive Assignment. This tailors auto-assignment to their needs if they find Predictive to be too aggressive, or isolate the results of a particular strategy. Lastly, users now have the ability to upload additional training data CSV files based on previous semester final assignments to keep the Historical assignment logic relevant to ongoing changes to PKI's scheduling strategy. The users always have the ability to restore default training data if they accidentally add a non-finalized CSV or any CSV that degrades performance. They are warned to only provide final assignment data. Theoretically, they could even weight the input CSVs by uploading duplicates if desired.

Our List view now features customized columns and real-time search which returns results from any of the active columns. This means users can decide to search by classes that are unassigned, by department, room, any trend that exists in the available row data.

Our program has also been adapted to run locally and in production seamlessly. Any failed database connections results in fallback logic that allows the user to login with admin/password. This was achieved by using a base URL in the frontend, and using configuration files for this base URL that differ depending on how the FrontEnd is build.

To build the project for production and populate the static files to be uploaded to AWS S3, run: ng build --configuration=production
  -Navigate to the FrontEnd directory and find the "dist" folder which contains all necessary files to upload.

To build the frontend locally, navigate to the frontend directory and run: npx ng serve

Complete Instructions for running locally:
1. You may need to install dependencies listed in the previous release notes such as flask and pandas.
2. Open a terminal in your ide, or command line interface, and run the application.py in the BackEnd directory of the project.
3. Install NodeJS as necessary on your computer.
4. Open a new terminal and navigate to our projects FrontEnd folder. Run commands: 'npm install' and 'ng add @angular/material'.
5. Build and run the frontend with 'npx ng serve'.
6. Click the link in the terminal to load the webpage on your local.
7. Upload an input CSV file from the interface.
8. Navigate to http://localhost:4200 to view the results of the room assignments.

Local pip freeze > requirements.txt:

blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
flask-cors==5.0.1
Flask-JWT-Extended==4.7.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
mysql-connector-python==9.3.0
numpy==2.2.5
pandas==2.2.3
PyJWT==2.10.1
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
Werkzeug==3.1.3

All experimental code is contained in our Prototyping directory. This directory essentially contains a copy of the back-end project files. Any accepted prototypes are then transitioned into the larger project structure for implementation.

## RELEASE NOTES MILESTONE 4 (v0.4.19)

This fourth development release of our project features editing capability for class information, and automatic updates to conflict cards, ability to ignore/restore conflict cards, and a detailed view of each class in the details pane. You can export your changes to a CSV which is downloaded from the browser, you can register an account, and logging in is restricted without correct credentials which are stored in a persistent relational database. The entire project has been implemented on Amazon Web Services using Elastic Beanstalk to dynamically create EC2 servers based on demand, an EC2 server to host our database which is managed in AWS RDS, and our frontend is hosted using an S3 bucket.

Shortcomings of this milestone include our assignment files, which were to be stored in our database so you can save changes to an assignment model for later access. We also weren't able to implement our workspace model to remeber which columns were selected by the user to be displayed, among other platform settings such as which view the user is on.

All updated code is in our main branch, and no additional branches need to be considered to use the program.

Instructions for running on AWS:

Simply access the provided link when the project is actively hosted. This is unfortunately costly and is only available for a certain scheduled time by request.

Instructions for running locally:
1. You may need to install dependencies listed in the previous release notes such as flask and pandas.
2. Open a terminal in your ide, or command line interface, and run the application.py in the BackEnd directory of the project.
3. Install NodeJS as necessary on your computer.
4. Open a new terminal and navigate to our projects FrontEnd folder. Run commands: 'npm install' and 'ng add @angular/material'.
5. Build and run the frontend with 'npx ng serve'.
6. Click the link in the terminal to load the webpage on your local.
7. Upload an input CSV file from the interface.
8. Navigate to http://localhost:4200/data to view the results of the room assignments.


## RELEASE NOTES MILESTONE 3 (v0.3.31)

This third major release of our project has a more polished experience for the user. Uploading a CSV into the platform will automatically bring the user to the section/list view, populate the data rows, and display all conflicts after automatic assignment was attempted.

For our milestone 3 we had the goals of improving assignment logic, building out key interface components, login page redesign, registration page design, expanding conflict types, state management, authentication, and file management. We achieve many of these goals but we weren't able to complete authentication due to its dependency on a relational database in our production environment, whereas our project is still being developed locally. The backend has been transistioned to the production environment and the database is under construction.

What we achieved: login page has been redesigned, a registration page has been designed, our section/list view of classes is mostly completed aside from column sorting and customization, conflict cards are populated into the conflict manager, assignment files now store information necessary to save progress (saving not yet implemented), performance improvements have been made to avoid re-processing of data.

All updated code is in our main branch, and no additional branches need to be considered to use the program.

Instructions for running locally:
1. You may need to install dependencies listed in the previous release notes such as flask and pandas.
2. Open a terminal in your ide, or command line interface, and run the application.py in the BackEnd directory of the project.
3. Install NodeJS as necessary on your computer.
4. Open a new terminal and navigate to our projects FrontEnd folder. Run commands: 'npm install' and 'ng add @angular/material'.
5. Build and run the frontend with 'npx ng serve'.
6. Click the link in the terminal to load the webpage on your local.
7. Upload an input CSV file from the interface.
8. Navigate to http://localhost:4200/data to view the results of the room assignments.

## RELEASE NOTES MILESTONE 2 (v0.2.28)

This second major release of our project showcases a homepage design for our user interface for scheduling classes. The user can upload a CSV file and our automatic scheduler will attempt an assignment model based on first-generation scheduling logic.

For our milestone 2 we had the goals of CSV upload functionality from the frontend to the backend, class asignment through rudimentary logic, output CSV generation (export functionality), course/room allocation conflict identification and data input error identification, and test functionality and basic testing prototypes. We achieved evverything on our milestone 2 goal sheet except for frontend input validation. Caveats include unintuitive methodology for uploading a CSV and assigning classes. A user needs to browse their filesystem for the CSV and there is no upload button-- then the user navigations to index/data to actually call the assignment logic. In the future this will be more interface-friendly and this iteration is to show the state of functionality for these ideas.

All updated code is in our dev branch, and no additional branches need to be considered to use the program.

Instructions for running locally:
1. You may need to install dependencies listed in the previous release notes such as flask and pandas.
2. Open a terminal in your ide, or command line interface, and run the application.py in the BackEnd directory of the project.
3. Install NodeJS as necessary on your computer.
4. Open a new terminal and navigate to our projects FrontEnd folder. Run commands: 'npm install' and 'ng add @angular/material'.
5. Build and run the frontend with 'npx ng serve'.
6. Click the link in the terminal to load the webpage on your local.
7. Upload an input CSV file from the interface.
8. Navigate to http://localhost:4200/data to view the results of the room assignments.

## RELEASE NOTES MILESTONE 1 (v0.1.25)

This first release focuses on our data models and their basic manipulation to display information comprehensively (row/column format). We can populate all course sections into objects and extract the necessary data for display. Current implementation displays the following attributes of a course-section: Catalog Number, Section Number, Room, Enrollment Count, and Max Enrollment.

At this early stage, front-end development is largely decoupled from the back-end. We have demonstrated passing information between the two using an API call, but no significant functionality has been completed on the front-end, which is currently in an aesthetic design phase. Follow instructions in `Documentation` > `Angular Setup.txt` to run the login page.

Our web server (deployed on AWS Elastic Beanstalk) scales according to user demand automatically. So far, testing has been limited to the IDE using prototype files or via localhost, though the production server is implemented and available to test on. To test the web platform, simply run the `application.py` file located in the `BackEnd` directory. (You will need to install the required Python libraries as documented in the Libraries file in the Documentation directory of the project.) Instructions for establishing a python virtual environment (venv) can be found in `Documentation` > `Python Setup.txt`

### Current Libraries:
1. flask
2. gunicorn
3. flask_jwt_extended
4. pandas
5. flask-cors

### Current Data Models:
- **CourseSection:** Allows us to build objects that represent each course section and manage data as needed. All relevant columns are extracted from the input CSV and converted into CourseSection objects for sorting and modification.
- **Classroom (prototype):** Enables us to determine attributes and constraints of rooms to decide whether a CourseSection can be assigned there.

## BRANCH DISTINCTION

We decided to have everyone create their own branch as an offshoot from the dev branch. We often calibrate our work by merging to the dev branch, and pulling from it to get the latest project information. Specific branches have not been created for the sole purpose of testing a specific feature.

main        -> Release candidates
dev         -> All development activity that is not a candidate for release
dev-tyler   -> Backend data models, data model factories, flask routing, utility modules, controller modules, input spreadsheet analysis, classroom attribute analysis, commands for initialization and management of Github, the Python virtual environment, Angular, Elastic Beanstalk, and an account of the python libraries considered and implemented for the project. Frontend work was also done on components including typescript, HTML, and SCSS.

dev-Haresh  -> Responsible for creating the home page, and creating the outline for the overall lateout of the website,  conflicts tabs, profile button, files tab, data extraction, data formatting, and assignment logic

dev-Haresh1 -> Branch that was created to be up-to date with main to be eventually merge to main.

dev-Haresh2 -> Created the Login, and the registration page (using mat-cards instead of manually css ), Added a cool background for the login page.

dev-Haresh3 -> Made the logic behind validating account creation under registration.

dev-trevor  -> Mainly used for initial implementation of the front end design and shifted more towards front end logic and development as we got further into the project. Main features like our API connection, upload, list view, details (which was overhauled by tylers branch), and calendar view were all initialized in this branch and further expanded on by other branches after being moved to the development branch. This branch was also used to tweak design SCSS and logic between front end components.

dev-honora  -> Data analysis, focusing largely on parsing an extremely extensive JSON of scheduling data provided by the project sponsor. From this we were able to create a frequency map to show which departments were most often assigned to which rooms. This was used in the auto-assignment logic as the most accurate method of assignment, though it usually assigns the least amount of classes.

dev-fara    -> This branch was primarily used for backend  testing. It included the implementation of backend test cases using Pytest, specifically for validating the logic around the Classroom and Section objects and ensuring correct API functionality.

dev-fara2	-> This branch was created to stay up to date with both the main and dev branches. It acted as an integration point to test and resolve any merge conflicts before pushing updates to the mainline.

Sphinx_doc  -> This branch was used to develop and maintain backend documentation using Sphinx. It includes auto-generated API documentation and descriptions of backend modules to improve code maintainability and onboarding for new developers.

rc-1        -> release candidate 1 was created to keep the production implementation separate from the dev branch, to avoid breaking local implementation for other developers while migrating to AWS. This branch became redundant when we switched all hard-coded urls to ${environment.apiBaseUrl}... for example ${environment.apiBaseUrl}/edit/save/${courseId}

e2e-test    -> This branch was dedicated to implementing end-to-end testing using Cypress. It covered user flows such as authentication, CSV uploads, conflict detection, and interaction with the scheduling interface to ensure the full application workflow functioned as intended.

docs-cleanup->  Initially created to resolve formatting and structural issues in the backend documentation, this branch became redundant after those issues were incorporated into the Sphinx_doc branch. As a result, Sphinx_doc now fully replaces the need for docs_cleanup.


## 📘 Documentation

### Frontend Documentation 
- [Frontend Docs](https://resonant-concha-a76f32.netlify.app/)

### Backend Documentation
- [Backend Docs](https://glistening-genie-2e3b4d.netlify.app/)
