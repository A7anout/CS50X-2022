# TODO LIST
#### Video Demo:  [Click me](https://youtu.be/2ovnxIRJEgU)
#### Description:

## Background
Alright this is CS50 and this already my final project and inspired from the psets (problem sets) I made a website called “TODO LIST ” in which a user can easily add/delete some tasks to do with a date due.

## Understanding

So let’s start with the templates.

### layout

Inside of "layout" is the layout of the rest of the pages(which I will talk about soon) and you can see that I mostly copy pasted from Bootstrap just to make the website a little prettier. Next you can notice that I use some jinja to decide the navbar depending if the user is logged in or not. After that comes also some jinja to extend some other pages. Next is the footer which has some of the links like facebook, instagram and discord which refer to CS50 communities.

### features

So this is the first page that the use can actually see which descripes some the website features

### register

The next page the user is probably going to use is register which allows the user to create an account on the website but unlike finance pset, I made the username and password fields required so that I don't have to apology to them if they just leave those fields. But I did use the apology function from finance to alert the user if the name is already taken and/or the passwords don't match.

### login

After the user register, the next step is to log in with his new account. Also I made the username and password required so I don't have to apology if he leaves them blank. But again I used the apology function in case the user types invalid username and/or password.

### index

Index is the main page of the website but it doesn't really do much. It just says welcome user and asks if they want to add anything to their list

### add

Here the user can actually add any row to their list. Notice that only the event description is required but otherwise the user is free to leave the due date and/or the importance empty.

### list

Once the user has successfuly added an event to their list, they are redirected to this page where they can see all the events they added before and they can also remove any of them using the remove button.

Now let's see some actual code

### helpers.py

As in finance I needed a second app with some other functions to help me with the main app. This app has only two functions.

#### apology

Which is already familiar from finance and it's used only when the user tries to register with an already existing username or the passwords don't match

#### login_required

This function is used so that non logged in users can't access to some pages that they shoudln't so they are redirected to the features page

### app.py

As always I started with some frameworks and libraries that I'm going to use later like cs50 and others. I used flask as in finacne then I made sure the templates are auto reloaded so I don't have to keep stopping and running flask. After that I used the CS50 library to use SQLite for my database.

#### after_request

This is the first function which ensure responses aren't cached.


#### /

So here is the index function which takes the username from the database just to say welcome to the user

#### /register

Register function takes to method. The first one is if the user is trying to make an account so it handles making an apology to user if he used an already used username and/or they didn't confirm with the same password. The other method is when the user just goes to the page (with a link or some other way).

#### /login

I actually copy pasted this function from finance but made some small changes

#### /features

Nothing important to see here

#### /list

Notice now that this function uses another function login_required so if a user that's not logged in can never get into this page. Also this function takes two methods. But POST here is actually used if the user wants to remove a row from the list

#### /add

This is the last function which is used if the user wants to add a new row to the list. Notice that also this function use login_required so only logged in users can add to their list.