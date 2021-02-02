from registration import db, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from registration import login_manager
from flask_login import UserMixin
from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
from hashlib import md5

#required for azure blob service
blob_container = app.config["BLOB_CONTAINER"]
storage_url = f"https://{app.config['BLOB_ACCOUNT']}.blob.core.windows.net/"
storage_key = app.config["BLOB_STORAGE_KEY"]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_image = db.Column(db.String(40), default="user.png")
    
    def __repr__(self):
        return f"User <{self.username}>"

    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_photo(self, file):
        if file:
            #use secure_filename for system security
            filename = secure_filename(file.filename)
            filename_, file_extension = filename.rsplit('.',1)
            # change the user photo name to his email and hash it
            filename_ = md5(self.email.encode('utf-8')).hexdigest()
            filename = filename_+'.'+file_extension
            
            # connect to azure blob storage and upload the file
            blob_service = BlobServiceClient(
                account_url = storage_url,
                credential = storage_key)
            blob_client = blob_service.get_blob_client(
                container = blob_container,
                blob = filename)
            
            #upload file to azure
            blob_client.upload_blob(file)
            self.user_image = filename


