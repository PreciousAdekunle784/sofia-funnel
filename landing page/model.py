from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ... keep your existing imports and db setup ...

class User(UserMixin, db.Model):
    """
    Admin User Table.
    Stores secure credentials for dashboard access.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Create a secure hash of the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

# ... keep your existing Lead and Application classes ...