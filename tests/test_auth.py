import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    assert response.status_code == 302  # Redirect to login
    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'

def test_login(client):
    with client.application.app_context():
        user = User(username='testuser', email='test@example.com')
        user.password = 'password'  # Use the password property setter to hash the password
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 302  # Redirect to dashboard

def test_logout(client):
    with client.application.app_context():
        user = User(username='testuser', email='test@example.com')
        user.password = 'password'  # Use the password property setter to hash the password
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to index
