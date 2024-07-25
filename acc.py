from flask import Flask, request, redirect, url_for, render_template, flash

#Imports for the dataabase functionality of the website.
from flask_sqlalchemy import SQLAlchemy

#'LoginManager' imports relate to features for the current user and current session of the website.
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

#import used for handling dataabse changes
from flask_migrate import Migrate






#Creating the flask application instance and naming it 'app'.
app = Flask(__name__)

#telling where the database is located. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyBuddy.db'
#The 'secret key' is used with a session for security.
app.secret_key = 'aaa'  






#Creating a SQLAlchemy object and naming it 'db'. Passing in this app so that it can work with it.
db = SQLAlchemy(app)


migrate = Migrate(app, db)

#passing in this app to the 'LoginManager' so that user sessions can be managed
login_manager = LoginManager(app)






#loading the user when the app needs to check who is currently logged in. Getting a user object from the 'User' table by passing the id
#and querying the database.
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)





#creating the database table to store every user who makes an account.
#Each user has an id so that their details and flashcards can be uniquely identified.
#Setting each of the columns in the table.
class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    studyField = db.Column(db.String(60), nullable=False) 
    studyYear = db.Column(db.String(1), nullable=False)





#creating the database table for a users flashcards. Whent the user creates a flashcard, the
#text and colour are saved to a flashcard object which is tied to a users id so that
#the card can be displayed on the users homepage as well
class flashCard (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    textColour = db.Column(db.String(7), default='#FFFFFF')
    backgroundColour = db.Column(db.String(7), default='#FFFFFF')
    




#setting the root URL of the website to the 'login' page which should be the first page shown. Users have
#to login to use the website.
@app.route("/", methods=['POST', 'GET'])
def index():
    return redirect(url_for('login'))






@app.route("/createCard/", methods=['POST', 'GET'])
def createCard():

    #checking if the user has pressed the button on the 'create card' page to submit the form.
    if request.method == 'POST':

        #the user enters the info into the form and we use the 'request' function to get it from the inputs in the 'createCard' page to 
        #apply it to this new flashcard. 
        newQuestion = request.form['cardQuestionText']
        newAnswer = request.form['cardAnswerText']
        newTextColour = request.form['cardTextColour']
        newBackgroundColour = request.form['cardBackgroundColour']

        #a new flashcard object is created and it's 'userId' variable is set to the id of the current user so that they can access it every time they log in. The other flashcard properties are gotten from the 'request.form' lines.
        newFlashcard = flashCard(userId = current_user.id, question = newQuestion, answer = newAnswer, textColour = newTextColour, backgroundColour = newBackgroundColour)


        #Adding the new flashcard information to the session to be ready to commit changed.
        db.session.add(newFlashcard)
        #sending these changes to the database so that they are saved. These
        #flashcards will be able to be displayed in the homepage by loading them from the database and
        #recreating them.
        db.session.commit()




    #linking to the relevant html file for this page.
    return render_template('htmlTemplates/createCard.html')





#getting the flashcardId from the javascript file and setting it to an integer variable so we can use it.
@app.route("/deleteFlashcard/<int:flashcardId>", methods=['POST'])
def deleteCard(flashcardId):


    #getting the specified flashcard from the database by comparing the id's to my integer variable to find the correct id
    flashcardToDelete = flashCard.query.get(flashcardId)

    #code to delete the flashcard from the database and then save changes.
    db.session.delete(flashcardToDelete)
    db.session.commit()






@app.route("/signup/", methods=['POST', 'GET'])
def signup():


    #defining the error message variable so I can give it a value and use it.
    errorMessage = None;
    #checking if the user has submitted the form on the webpage
    if request.method == 'POST':


        #the user enters their info into the form page and the info is received from the forms input fields. These values are set to variables to be used further down to create a new user in the User table.
        newUsername = request.form['username']
        newPassword = request.form['password']
        newStudyField = request.form['studyField']
        newStudyYear = request.form['studyYear']

       #checking the list of users to see if a username is already taken. 
        existingUser = User.query.filter_by(username=newUsername).first()
        if existingUser:
           errorMessage = 'A user with this username already exists.'
        else:

        #creating a new user by setting the new users attributes to the ones that were entered in the form. Then adding this
        #new user to the User table in the database.
           newUser = User(username=newUsername, password=newPassword, studyField=newStudyField, studyYear=newStudyYear)
           db.session.add(newUser)
           db.session.commit()
           return redirect(url_for('login'))
    #linking to the relevant html file for this page. Assigning my custom error message text to the webpage.
    return render_template('htmlTemplates/signup.html', errorMessage = errorMessage)










@app.route("/login/", methods=['POST', 'GET'])
def login():


    #set to none so that the releavant message can replace the 'none' and be displayed.
    errorMessage = None
    if request.method == 'POST':
    

        #the user enters the info into the form and we use the 'request' function to get it from the /login/ to set it to a new user and add it to the database.
        loginUsername = request.form['username']
        loginPassword = request.form['password']


        #querying the 'User' table to find the user with the specified username.
        user = User.query.filter_by(username = loginUsername).first()


        #have to check if the user exists in the database, otherwise an error is displayed.
        if user:

            #then simple string comparison check to see if the password of this user has been entered correctly.
            if  user.password == loginPassword:

                #using an import from 'flask_login' to handle loggin in a user
                login_user(user)
                return redirect(url_for('homepage'))
            
           #if the user is correct but the password wrong, then this displays as the error message
            else:
                errorMessage = 'You have entered the wrong password.'


        #if the user is not valid, them this displays as the error message
        else:
            errorMessage = 'User does not exist.'

        
    
    return render_template('htmlTemplates/login.html', errorMessage = errorMessage)









@app.route("/homepage/", methods=['POST', 'GET'])
def homepage():

    #Getting all the flash card objects associated with the current logged in user so that all the flashcards they have made
    #will be displayed om the home page. It does this by linking the current logged in users ID to the one in my database. Then gets all flashcards for that user.
    homepageFlashcards = flashCard.query.filter_by(userId=current_user.id).all()


    
    #Linkiing to the relevant html file for this page so that it will display. I am also passing the flashcards to the template so that they will be displayed when we render template.
    return render_template('htmlTemplates/homepage.html', homepageFlashcards=homepageFlashcards)



    





@app.route("/accountInfo/", methods=['POST', 'GET'])
def updateAccount():


    errorMessage = None;
    if request.method == 'POST':

        #the user enters their new account info into the form on the webpage and we use the 'request' function to get the new info from the
        #text boxes on the account page and assign them to a variable to be used later in the code.
        newUsername = request.form['username']
        newPassword = request.form['password']
        newStudyField = request.form['studyField']


        #checking the list of users to see if a username is already taken.
        existingUser = User.query.filter_by(username=newUsername).first()

        if existingUser and existingUser.id != current_user.id:
           errorMessage = 'A user with this username already exists.'
        else:
 
           #using 'flask_login' import to get the current users username, password and studyField. Then replacing the current values with the ones from the update form using the values in the 'new' variables from earlier.
           current_user.username = newUsername
           current_user.password = newPassword
           current_user.studyField = newStudyField
        

           #saving changes to the database so that these changed are stored and remembered.
          
           db.session.commit()
    

    return render_template('htmlTemplates/accountInfo.html', errorMessage = errorMessage)








@app.route("/logoutAccount/", methods=['POST'])
def logoutAccount():


    #Used from 'flask login' to log out the user.
    logout_user()
    #When the user logs out, this moves them out the website and back to the login page automatically.
    return redirect(url_for('login'))








@app.route("/deleteAccount/", methods=['POST'])
def deleteAccount():

    
    #using the 'flask_login' import to get the user currently logged in.
    db.session.delete(current_user)
    db.session.commit()

    return redirect(url_for('login'))







@app.route("/findBuddy/", methods=['GET', 'POST'])
def findBuddy():
    
        
    #using 'join' to connect the 'User' and 'flashCard' tables. This is because I need to look at the 'studyField' attribute in the 'User' table to get the flashcards from the 'flashCard' table. Excluding the flashcards from the current user because these should not be repeated in the 'findBuddy' page. 
    buddyFlashcards = flashCard.query.join(User).filter(
            User.studyField == current_user.studyField,
            User.id != current_user.id).all()


    return render_template('htmlTemplates/findBuddy.html', buddyFlashcards = buddyFlashcards)





if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)






