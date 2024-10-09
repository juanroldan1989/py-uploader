from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import boto3
import os

from models import FileRecord
from forms import UploadForm
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME, S3_BUCKET_URL, FLASK_SECRET_KEY, POSTGRES_URI

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

db = SQLAlchemy(app)

# Initialize S3 client
s3 = boto3.client(
  "s3",
  aws_access_key_id=AWS_ACCESS_KEY,
  aws_secret_access_key=AWS_SECRET_KEY
)

# Route for uploading files
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
  form = UploadForm()

  if form.validate_on_submit():
    file = form.file.data

    # Save file locally
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Upload file to S3 bucket
    s3.upload_file(file_path, S3_BUCKET_NAME, file.filename)

    # Save file metadata to PostgreSQL database
    new_file = FileRecord(file_name=file.filename, s3_url=f"{S3_BUCKET_URL}/{file.filename}")

    db.session.add(new_file)
    db.session.commit()

    flash("File uploaded successfully")
    return redirect(url_for("upload_file"))

  return render_template("upload.html", form=form)

# List of uploaded files
@app.route("/files", methods=["GET"])
def list_files():
  files = FileRecord.query.all()
  return render_template("files.html", files=files)

if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)
