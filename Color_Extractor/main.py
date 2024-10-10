from addit_methods import get_file_path, find_img_colors, allowed_file
from forms import UploadForm

from flask import Flask, render_template
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
import os
import uuid

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('MARKET_APP_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    default_file_name = 'main-page.jpg'
    file_name = default_file_name
    path = get_file_path(file_name)
    color_dict = find_img_colors(path)

    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            # Generate a unique filename
            filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
            path = get_file_path(filename)
            file.save(path)
            color_dict = find_img_colors(path)

            return render_template('index.html', image_file=filename, form=form, colors=color_dict)
        else:
            return render_template('index.html', form=form, image_file=default_file_name, error="Unsupported file type",
                                   colors=color_dict)

    return render_template('index.html', form=form, image_file=default_file_name, colors=color_dict)


if __name__ == '__main__':
    app.run(debug=True)
