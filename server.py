import os, flask, zipfile, shutil
from werkzeug.utils import secure_filename
from src.gen_pic import BinPics
app = flask.Flask(__name__)
env_dir = "./upload_folder"
res_dir = "./res_folder"
tmp_dir = "./tmp_folder"
ret_dir = "./ret_folder"


binPics = BinPics(res_dir, tmp_dir)

def convert_back(f_name):
    """
    get the file name and convert back from pngs to normal file
    """
    pic_dir = os.path.join(res_dir, f_name)
    for root, _, files in os.walk(pic_dir): 
        for file in files: 
            pic_f = os.path.join(root, file)
            ret_f = os.path.join(tmp_dir, file)
            binPics.read_file(pic_f, ret_f)


    # by now, the files should already be convert back
    # merge the files together
    ret_f = os.path.join(ret_dir, f_name)
    os_command = f"cat {tmp_dir}/*.png > {ret_f}"
    os.system(os_command)
    return ret_f

def setup_env():
    os.makedirs(env_dir, exist_ok=True)
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    os.makedirs(ret_dir, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    file_path = None
    file_name = None 
    # clear the tmp folders
    os.system("./clean.sh")
    setup_env()
    try:
        uploaded = flask.request.files
        print(uploaded)
        for file_values in uploaded.listvalues():
            # we only have one key here
            for f in file_values:
                file_name = secure_filename(f.filename)
                file_path = os.path.join(env_dir, secure_filename(f.filename))
                f.save(file_path)
    except Exception as e:
        print(e)
        return "File uploading failed"

    print("Try to split the file")
    target_filename_dir = os.path.join(tmp_dir, f.filename)
    binPics.split(file_path, target_filename_dir)
    print("Split finished. Try to convert to images")
    target_files = sorted(os.listdir(target_filename_dir))

    # make the res folder
    res_filename_dir = os.path.join(res_dir, file_name)
    os.makedirs(res_filename_dir, exist_ok=True)

    for f in target_files:
        cur_f = os.path.join(target_filename_dir, f)
        res_f = os.path.join(res_filename_dir, f + '.png')
        binPics.gen_pic(cur_f, res_f)

    # create zip file for download
    # command injection every where
    os_command = f"zip -r pictures.zip {res_filename_dir}/*.png"
    os.system(os_command)
    return "success"

@app.route("/backtofile", methods=['POST'])
def back_to_file():
    file_path = None
    file_name = None
    os.system("./clean.sh")
    setup_env()
    try:
        uploaded = flask.request.files
        print(uploaded);
        for file_values in uploaded.listvalues():
            print(file_values)
            # we only have one key here
            for f in file_values:
                file_name = secure_filename(f.filename)
                file_path = os.path.join(env_dir, secure_filename(f.filename))
                f.save(file_path)
        print(file_path)
    except Exception as e:
        print(e)
        return "File uploading failed"
    pic_dir = os.path.join(res_dir, file_name)
    with zipfile.ZipFile(file_path) as zf: zf.extractall(pic_dir)
    rfile_path = convert_back(file_name)
    shutil.move(rfile_path, './file')
    return "success"


@app.route("/converted", methods=['GET'])
def get_converted():
    return flask.send_from_directory('./', 'pictures.zip')

@app.route("/backed", methods=['GET'])
def get_back():
    return flask.send_from_directory('./', 'file')

@app.route('/', methods=['GET', 'POST'])
@app.route('/css/<path:cssname>', methods=['GET'])
@app.route('/imgs/<path:imgname>', methods=['GET'])
def index(cssname=None, imgname=None):
    if not cssname:
        return flask.send_from_directory(app.static_folder, 'index.html')
    elif cssname:
        return flask.send_from_directory(os.path.join(app.static_folder, 'css'), cssname)
    elif imgname:
        return flask.send_from_directory(os.path.join(app.static_folder, 'imgs'), cssname)

app.run(host='0.0.0.0', port=9870)
