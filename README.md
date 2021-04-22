ENGO 551
Winter 2021

Final Group Project

By:
Alekhya Bhamidipati
Madison Marriott
Tanya Hegmann
-----------------------------------------------------------------
To run this code on the computer, navigate to the folder containing the files and open the cmd window

Please run 
py -m pip install -r requirements.txt //Folder containing requirements
py -m pip install requests

set FLASK_APP=application.py
set FLASK_DEBUG=1
set DATABASE_URL=postgres://kevshpuonrwgfr:c8535cc284c9df961ecf0aa1657793e8de1632987c584b02216bbe401f4cb6f3@ec2-54-205-183-19.compute-1.amazonaws.com:5432/d67i21u3n79vhb
And then to run the code: 
py -m flask run

-----------------------------------------------------------------
There are 8 Webpages for this website:

/ 
- The Home Page
- Greets the User Upon Coming to the Website
- Has a google maps API of Calgary for bonus
- If a user session is detected, load template homesignedin.html 
	- Prompts a signed in user to search a community or log out
		- Logged out users are taken to /logout
		- Users looking to search a community are taken to /calgarycommunityhousingmap
- If no user session is detected, load template home.html
	- Prompts a user to sign up or sign in  
		- If a user signs in they are taken to /signin
		- If a user signs up they are take to /signup


/signin
- Allows users to sign in to a pre-existing account to access the website
- User is loaded in signin.html
- Users can sign in with a username and password
	- Upon signing in they are taken to /signincheck
- Option for user to return to home page
	- User is taken to /
- Option for user to go to Sign-Up instead
	- User is taken to /signup


/signincheck
- The credentials entered by users in /signin are checked against the database for username/password match
- If credentials are correct, user is loaded signinsuccess.html
	- The user is notified that they have succesfully signed in with their username
	- The user had the option to
		- Return to home going to / 
		- Log out of their account going to /logout
		- Search Calgary communities going to /calgarycommunityhousingmap
- If credentials fail and sign in fails user is loaded signinfail.html
	- The user is told their sign in failed with that username
	- The user has the option to
		- Return to home going to / 
		- Signing in again going to /signin
		- Signing up a new account going to /signup


/signup
- Allows users to sign up to a pre-existing account to access the website
- User is loaded in signup.html
- Users can sign in with a username and password
	- Upon signing up they are taken to /signupcheck
- Option for user to return to home page
	- User is taken to /
- Option for user to go to Sign-In instead
	- User is taken to /signin


/signupcheck
- The credentials entered by users in /signup are checked against the database for if the username is taken
- If credentials are correct, user is loaded signupsuccess.html
	- The username is stored in the database
	- The user is notified that they have succesfully signed up with their username
	- The user had the option to
		- Return to home going to / 
		- Log out of their account going to /logout
		- Search Calgary communities going to /calgarycommunityhousingmap
- If credentials fail and sign in fails user is loaded signupfail.html
	- The user is told their sign up failed with that username
	- The user has the option to
		- Return to home going to / 
		- Signing in to a pre-existing account going to /signin
		- Try Signing up a new account again going to /signup


/logout
- The user logs out and the session ends
- The user has the option to 
	- Return to home going to / 
	- Signing in to a pre-existing account going to /signin
	- Sign up with a new account going to /signup


/calgarycommunityhousingmap
- The Main website page for the user
- Contains the main interactive map application (more details below)
- The user has the option to 
	- Return to home going to / 
	- Refresh the page/map and return to /calgarycommunityhousingmap
	- Log out go to /logout
	- Return to top of page (if at bottom of page)



/api/SELECTEDCOMMUNITY
- Returns the average residential property value and community code for the community specified in the route
- The community name must be in all capital letters


-----------------------------------------------------------------
Information on the Map:

Once a community is selected from the dropdown form, the map will update with information:

- The selected community boundary will be highlighted and outlined
- The nearest hospital, EMS, Police, and Fire stations to the community will appear as markers
- Parks and Schools within the community will appear as markers
- A marker will appear if a community contains a flood prone region
- A user can estimate the commute time driving from the selected community to any location by clicking the map, a popup will be generated indicating the time in minutes







