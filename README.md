#QRIFY
#### Video Demo:https://youtube.com/watch?v=-T6ku7kmqJg&feature=share
#### Description:
QRify is a web application that allows users to generate QR codes for their desired URLs and save them to their account for later use.

#Features
    User Registration
    User Login
    Generate QR codes
    Download QR codes
    Store QR code information (URL and name) in database
    View saved URL links

#Tech Stack
    HTML, CSS and Flask for front-end and back-end development
    SQLite3 for database management
#Requirements
    Flask
    SQLite3

It is a QR code generator which helps user create their own QR code.
Here the user can register for a new account which will be stored into the database , user can login to their previous accounts if they have one.
Now as the user is logged in , he/she has to paste the URL and name for the URL of which they want to create the QR code.
Now click on the "Generate QR " button, it will prompt the user to next page which contains the QR .
Here the user can download the QR to their local systems .
The generated QRs URL links and their names will be stored into our database .
If the user wants to look for the previous QRs the , he / she can click on "View QR" tab which will prompt the user to another page which contains all the previously saved QRs URL and their respective names . 
This was Qrify

The structure and design of this project is inspired from the finance problem from CS50 as I was struggling with creating the styles and CSS of this project . 

#Running the project
    Make a copy of this project into your local systems
    install all the dependencies and libraries using pip
    then open the flasks virtual environment
    then type command - flask run to run the project on localhost://5000
    you can view the running project on the respective port .

Thankyou.
