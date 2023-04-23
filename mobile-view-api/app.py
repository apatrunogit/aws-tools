import boto3
from flask import Flask, request, redirect

app = Flask(__name__)

s3 = boto3.client('s3')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        s3.upload_fileobj(file, 'your-bucket-name', file.filename)
        return redirect('/')
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
