from app.models.file import File
from app import db
import os


def get_all_files():
    try:
        files = File.query.all()
        return files
    except Exception as e:
        print(str(e))
    return None


def get_file_by_id(id):
    try:
        file = File.query.filter_by(id=id).first()
        return file
    except Exception as e:
        print(str(e))
    return None


def save_file(file, path, filename):
    try:
        fullpath = os.path.join(path, filename)
        file.save(fullpath)
        f = File(name=filename, path=fullpath)
        db.session.add(f)
        db.session.commit()
    except Exception as e:
        print(str(e))


def delete_file(id):
    try:
        file = File.query.filter_by(id=id).first()
        path = file.path
        db.session.delete(file)
        db.session.commit()
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(str(e))