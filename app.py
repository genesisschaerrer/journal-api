from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app= Flask(__name__)

# Tester code to see if app is working. make sure you are in a pipenv shell and run your script 
# @app.route('/')
# def hello():
#     return "Got Here"

# if __name__ == "__main__":
#     app.run(debug=True)
#Once youve reached step 17 you can delete this block of code.

#We are telling flask in our server where the application is located
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma= Marshmallow(app)


#create schema
# the class is a row and with the schema we are building the columns.
#the second argument primary_key  it allows you to have that item be unique. it cant repeat and automatically increments the id.
# Variable name = db.Column(db.(the datatype)(add max amount of letters), unique = False or true meaning can they repeat or not)
class JournalEntries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(1000), unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content 


class JournalEntriesSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


#Now we will extantiate the Journal Entries Schema. We will use two variables. 
#One for when we are working with one Journal Entry
#The other for when we are working with multiple

journal_entry_schema = JournalEntriesSchema()
journal_entries_schema = JournalEntriesSchema(many=True)

#At this point refrence the cheat sheet where the next step will be to start a repl


#Endpoint to create a new JOURNAL ENTRY
#Import request and jsonify library
@app.route('/journalentry', methods = ['POST'])
def add_journalentry():
    title = request.json['title']
    content = request.json['content']

    new_journalentry = JournalEntries(title, content)

    db.session.add(new_journalentry)
    db.session.commit()

    journalentry = JournalEntries.query.get(new_journalentry.id)

    return journal_entry_schema.jsonify(journalentry)

    # once youve finished this endpoint make sure you run py app.py in pipenv shell to make sure you have no errors 


#Get all journal entries 
@app.route('/journalentries', methods=['GET'])
def get_journalentries():
    all_journalentries = JournalEntries.query.all()
    result = journal_entries_schema.dump(all_journalentries)
    return jsonify(result)


#Get one journal entry
@app.route('/journalentry/<id>', methods=['GET'])
def get_journalentry(id):
    journalentry = JournalEntries.query.get(id)
    return journal_entry_schema.jsonify(journalentry)


#Updating a journal entry
@app.route('/journalentry/<id>', methods=['PUT'])
def journalentry_update(id):
    journalentry = JournalEntries.query.get(id)
    title = request.json['title']
    content = request.json['content']

    journalentry.title = title
    journalentry.content = content

    db.session.commit()
    return journal_entry_schema.jsonify(journalentry)


#Deleting a journal entry
@app.route('/journalentry/<id>', methods=['DELETE'])
def journalentry_delete(id):
    journalentry = JournalEntries.query.get(id)
    db.session.delete(journalentry)
    db.session.commit()
    
    return journal_entry_schema.jsonify(journalentry)





if __name__ == "__main__":
    app.run(debug=True)