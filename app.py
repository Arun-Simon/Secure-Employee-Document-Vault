from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from io import BytesIO

from collections import defaultdict
from services.dynamodb_service import get_all_documents
from services.s3_service import download_file
from services.kms_service import decrypt_text
from services.dynamodb_service import get_documents
from services.secret_manager import get_secret
from services.kms_service import encrypt_text
from services.s3_service import upload_file
from services.dynamodb_service import save_document_metadata

app = Flask(__name__)

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if request.method == "GET":

        return render_template(
            "upload.html"
        )

    config = get_secret()

    bucket_name = config["bucket_name"]
    kms_key_id = config["kms_key_id"]
    table_name = config["table_name"]

    employee_id = request.form["employee_id"]
    document_type = request.form["document_type"]

    file = request.files["file"]

    file_content = file.read()

    encrypted_data = encrypt_text(
        file_content.decode(),
        kms_key_id
    )

    object_name = (
        employee_id
        + "/"
        + file.filename
        + ".enc"
    )

    upload_file(
        bucket_name,
        object_name,
        encrypted_data
    )

    save_document_metadata(
        table_name,
        employee_id,
        file.filename,
        document_type
    )

    return f"""
    <h2>Upload Successful</h2>

    Employee: {employee_id}<br>
    File: {file.filename}<br>

    <a href='/'>
        Home
    </a>
    """

@app.route(
    "/documents",
    methods=["GET", "POST"]
)
def documents():

    if request.method == "GET":

        employee_id = request.args.get(
            "employee_id"
        )

        if employee_id:

            config = get_secret()

            docs = get_documents(
                config["table_name"],
                employee_id
            )

            return render_template(
                "documents.html",
                documents=docs
            )

        return render_template(
            "documents.html",
            documents=[]
        )

@app.route(
    "/download/<employee_id>/<file_name>"
)
def download_document(
        employee_id,
        file_name):

    config = get_secret()

    bucket_name = config["bucket_name"]

    object_name = (
        employee_id
        + "/"
        + file_name
        + ".enc"
    )

    encrypted_data = download_file(
        bucket_name,
        object_name
    )

    decrypted_content = decrypt_text(
        encrypted_data
    )

    return send_file(
        BytesIO(
            decrypted_content.encode()
        ),
        as_attachment=True,
        download_name=file_name,
        mimetype="text/plain"
    )

@app.route("/employees")
def employees():

    config = get_secret()

    table_name = config["table_name"]

    documents = get_all_documents(
        table_name
    )

    employee_counts = defaultdict(int)

    for doc in documents:

        employee_counts[
            doc["employee_id"]
        ] += 1

    employees = []

    for emp_id, count in employee_counts.items():

        employees.append({
            "employee_id": emp_id,
            "document_count": count
        })

    return render_template(
        "employees.html",
        employees=employees
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )