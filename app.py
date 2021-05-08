from flask import Flask, make_response, jsonify, session, escape, request
import datetime
from insects_detection.insects_utils import insects_tools
from insects_detection.pic_utils import pic_tools

app = Flask(__name__)
app.secret_key = 'inetlab-insects-detection'


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
