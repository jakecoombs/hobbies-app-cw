# Web Coursework 3 - Hobbies Web Application Using Django, Python, Vue.js and Bootstrap

https://learnouts.com/student/cw/10/

## Group Members

### Jake Coombs - 190847005

Contributions:

- User (self) profile page
- User (other) profile page
- Hobby details page
- User list page
- EECS OpenShift Deployment

### Aaron Cuthbertson - 190075675

Contributions:

- Custom User model
- Ajax for auth (signup/login/logout)
- Ajax for friend requests
- Unit tests for login and signup

### Callum Spiller - 190833983

Contributions:

- Create Hobby model
- Ajax for User (filter by either id/city/age, url params)
- Ajax for Hobby
- Unit test for users/hobbies

### Ziyaad Mahmood - 160394461

Contributions:

- Login/signup page
- Delete Hobby
- Create new hobby

## EECS OpenShift Deployment

Url: https://group42-group42.apps.kube.eecs.qmul.ac.uk/

## Admin

- username: hobbyadmin
- password: hobbies1

## Test Users

1.  - `testuser`
    - `pass`
2.  - `testuser1`
    - `pass1`
3.  - `testuser2`
    - `pass2`
4.  - `testuser3`
    - `pass3`
5.  - `testuser4`
    - `pass4`

## Marking Criteria

- [x] Account creation and login working
- [x] Using Django's AbstractUser model and authentication framework
- [ ] Profile page included, with (editable) profile picture, email, city, dob and list of hobbies
- [x] Correct modelling of application data and relationships
- [ ] List of users with similar hobbies page included and working as expected
- [x] Using Ajax where required with Vue and fetch API
- [ ] Avoiding hard-coded URLs using URL reversing
- [x] Avoiding code duplication using template hierarchy and/or decorators where needed
- [x] Required unit tests included
- [x] App deployed to Openshift
- [x] README and requirements.txt files included with the requested information

## About the Application

### API

Django python server

- conda activate djangoServer
- Run server using `{py or python} manage.py runserver`
- Make migrations when changing a model using `{py or python} manage.py makemigrations`
- Run migrations after making migrations using `{py or python} manage.py migrate`

### Home View

Vue.js reactive front-end with Bootstrap for styling.

### Models

For each model, there is a to_dict() function which converts the model attributes to a Python Dictionary so that it can be handled much more easily in the API, and is organised to be returned as a JSON format.

For each model, there is an extra api value, which utilise the reverse() url function from django to return the url strings.
The api value points to the api function that can PUT changes and DELETE the object.
