# SPR 2024 CSCI4970-Capstone: Group 3\
# Peter Kiewit Institute Room Assignment and Scheduling Application

## ABOUT:

This web application is being developed to reduce the workload of the Classroom Coordinator responsible for assigning courses to rooms in the Peter Kiewit Institute (PKI) building at the University of Nebraska at Omaha.

Each semester, the Classroom Coordinator receives a CSV file containing all course sections that need room assignments in PKI. Difficulties arise when conflicts occur, and managing both scheduled and emergent conflicts has been shown to contribute to the high turnover in this role. We aim to automate as much of this process as possible and reduce the mental load on the user who utilizes our application to produce a finalized output CSV that is either conflict-free or allows conflicts to be ignored.

### We will achieve this by:

1. Automating assignments wherever possible and giving the user a choice of assignment methodologies to best suit their needs.
2. Identifying scheduling conflicts and presenting them to the user in an itemized list.
3. Employing quality-of-life features such as file management, allowing users to reload various drafts without losing data.
4. Allowing users to update building and room data to ensure constraints remain current with any future changes instituted by the college.

### Considerations:

1. Classroom Coordinators come and go, so our platform must cater to a diverse set of preferences and workflows to drive engagement and remain relevant to all users.
2. The input spreadsheet is part of a standardized course-section scheduling system used by many colleges, and our output CSV will conform to this format.

## RELEASE NOTES MILESTONE 1 (v0.1.1) 02/25/2025

This first release focuses on our data models and their basic manipulation to display information comprehensively (row/column format). We can populate all course sections into objects and extract the necessary data for display. Current implementation displays the following attributes of a course-section: Catalog Number, Section Number, Room, Enrollment Count, and Max Enrollment.

At this early stage, front-end development is largely decoupled from the back-end. We have demonstrated passing information between the two using an API call, but no significant functionality has been completed on the front-end, which is currently in an aesthetic design phase.

Our web server (deployed on AWS Elastic Beanstalk) scales according to user demand automatically. So far, testing has been limited to the IDE using prototype files or via localhost, though the production server is implemented and available to test on. To test the web platform, simply run the `application.py` file located in the `BackEnd` directory. (You will need to install the required Python libraries as documented in the Libraries file in the Documentation directory of the project.)

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

main        -> Release candidates\
dev         -> All development activity that is not a candidate for release\
dev-tyler   -> Focus on documentation, data models, data model factories, and flask routing\
dev-Haresh  -> Focus on data extraction, data formatting, and assignment logic\
dev-trevor  -> Front-end development and design\
dev-honora  -> Data analysis\
dev-fara    -> Data analysis

All experimental code is contained in our Prototyping directory. This directory essentially contains a copy of the back-end project files. Any accepted prototypes are then transitioned into the larger project structure for implementation. Currently, our most experimental prototyping is our logic to make use of our data models. Currently this means displaying information. In the future this will mean assigning rooms to course-sections and the logic to reason the appropriate assignments.