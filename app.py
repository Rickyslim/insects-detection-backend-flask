import os
import time
from flask import Flask, make_response, jsonify, session, send_from_directory, url_for, request, render_template, \
    current_app, abort, g, send_file
import datetime
from insects_detection.insects_utils import insects_tools
from insects_detection.pic_utils import pic_tools
from pathlib import Path
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from insects_detection.project_utils import project_tools
from insects_detection.file_manager import file_views

app = Flask(__name__)
app.register_blueprint(file_views, url_prefix="/view_files")
app.secret_key = 'inetlab-insects-detection'
app.config['JSON_AS_ASCII'] = False
app.config['REFRESH_MSEC'] = 1000
auth = HTTPBasicAuth()
bootstrap = Bootstrap(app)

@app.template_filter()
def file_filter(filefullname, file_name_part):
    if file_name_part == 1:
        return str(Path(filefullname).parent)
    if file_name_part == 2:
        return str(Path(filefullname).name)


@app.context_processor
def dir_processor():
    def format_logs_dir_to_multi(logs_dir):
        parent_dir_list = list()
        pa = Path(f'/{logs_dir}')
        while True:
            parent_dir_list.append({'url': url_for('file_views.index', logs_dir=pa.as_posix()[1:]), 'dir_name': pa.name[:]})
            pa = pa.parent
            if pa == Path('/'):
                parent_dir_list.append({'url': url_for('file_views.index', logs_dir=''), 'dir_name': '根目录'})
                break
        return parent_dir_list

    return dict(format_logs_dir_to_multi=format_logs_dir_to_multi)


@auth.verify_password
def verify_password(username, password):
    if username == 'user' and password == 'mtfy123':
        return True
    return False


# @app.route('/download/<path:fullname>', )
# def download_file(fullname):
#     current_app.logger.debug(fullname)
#     return send_file(f'{fullname}')
#     # return send_from_directory(f'/{logs_dir}',
#     #                            filename, as_attachment=True, )


@app.route('/')
def anything():
    return '???'


@app.route('/api/get_insects_info/<cached>')
@app.route('/api/get_insects_info/', defaults={'cached': 'c'})
def count_insects_from_gallery(cached):
    if "cached_insects_results" in session and cached == 'c':
        print(cached)
        response = make_response(session["cached_insects_results"])
    else:
        gallery_path = "D:\python\workspace\insects_detection\processed_imgs"
        gh_insects_info = insects_tools.green_house_insects_info(gallery_path)
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        gh_insects_info['update_time'] = time_str
        response = make_response(jsonify(gh_insects_info), 200)
        session["cached_insects_results"] = gh_insects_info
    return response


if __name__ == '__main__':
    app.run()
