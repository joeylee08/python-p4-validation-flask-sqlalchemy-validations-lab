from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, _, value):
        if not value:
            raise ValueError("You need a name, my friend.")
        elif Author.query.filter_by(name=value).first():
            raise ValueError("That author already exists!")
        else:
            return value
        
    @validates('phone_number')
    def validate_phone(self, _, value):

        pattern = re.compile(r'\D')

        if not isinstance(value, str):
            raise ValueError("Phone number must be a string.")
        elif len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.") 
        elif pattern.findall(value):
            raise ValueError("Phone number can only include digits.")
        else:
            return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, _, value):
        if not isinstance(value, str) or len(value) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        else:
            return value
        
    @validates('summary')
    def validate_summary(self, _, value):
        if not isinstance(value, str) or len(value) > 250:
            raise ValueError("Summary must be 250 characters or greater.")
        else:
            return value
    
    @validates('category')
    def validate_category(self, _, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        elif value != 'Fiction' and value != 'Non-Fiction':
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        else:
            return value
    
    @validates('title')
    def validate_title(self, _, value):

        clickbait_phrases = ['Won\'t', 'Believe', 'Secret', 'Top', 'Guess']

        if not isinstance(value, str):
            raise ValueError('Title must be a string.')
        else:
            for word in value.split():
                if word in clickbait_phrases:
                    return value
            raise ValueError('Title must contain one of the given clickbait words.')

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
