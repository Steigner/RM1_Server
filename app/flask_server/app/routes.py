# library -> flask
from flask import (
    Blueprint,
    Response,
    request,
    url_for,
    redirect,
    render_template,
    jsonify,
)

# library -> protect routes from no-authorized acces by wrapper
from flask_login import login_required

# script -> database model of patient database(ibm db2)
from .models import Patient

# script -> control camera - initialize camera for pre-defined settings
from .camera.cam_init import Camera_Init

# script -> control camera - streaming color, depth, infra
from .camera.func_stream_cam import StreamCam, StreamColorCam

# script -> control camera - faceID
from .camera.func_face_reco import FaceReco

# script -> control camera - face detection
from .camera.func_face_det import FaceDet

# script -> control camera - QR code reader, color camera
from .camera.func_qr_reader import ReadQR

# script -> control camera - taking point clouds
from .camera.func_take_pc import TakePC

# script -> get robot info via. socket communication
from .robot.get_data import Robot_info

# script -> store variables in back-end
from .store_tmp import StoreID, StoreIP, StoreCam, Counter, Validation, Point, Sim, Point2

# script -> detect server ip-adress(self ip adress)
from .self_ipadress import get_ip

# script -> post-processing took clouds
from .graph.graph_app import Show_PointCloud

# library -> encode blop file(image) from patient database(db2 database)
from base64 import b64encode

# library -> time manage
import time

# script -> processing identification of nostril from depth and color
from .camera.func_nostrill_det import NostrillDet

# script -> get current basic weather information
from .weather.weather import Weather

# set 1. blueprint = app
app = Blueprint("app", __name__)


# custom 401 handler
@app.errorhandler(401)
def custom_401(error):
    return render_template("401.html")


# custom 404 handler
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


# page -> route home:
# Note:
#   1. In this route is initialized camera if is pluged-in, if is not,
#   user has to make sure that camera is physically pluged-in and click on reload button,
#   also we store this fact.
#   2. Counter for how many times is reload this page.
@app.route("/home")
@login_required
def home():
    Counter.counter += 1

    Weather.download_weather()
    weather, temperature, preasure, humidity = Weather.get_weather()

    try:
        if Counter.counter == 1:
            info = Camera_Init().inicialize(c=True)

        else:
            info = Camera_Init().inicialize(c=False)

    except TypeError:
        info = "Camera status: device is not pluged-in"

    StoreCam.cam = info

    return render_template(
        "home.html",
        ip=StoreIP.ip,
        count=Counter.counter,
        cam=info,
        weather=weather,
        temperature=temperature,
        preasure=preasure,
        humidity=humidity,
    )
    # return render_template("home.html", ip=StoreIP.ip, count=Counter.counter, cam=info)


# ajax -> route ip adress:
# Note:
#   1. This route is called by ajax from js module ROS connect,
#   main purpose of this route is get self ip adress of server.
@app.route("/ip_adress", methods=["POST", "GET"])
@login_required
def ip_adress():
    if request.method == "POST":
        if request.form["value"] == "ip":
            return jsonify(get_ip())

        else:
            return jsonify("No ip")

    return redirect(url_for("app.home"))


# redirect page -> route reload:
# Note:
#   1. Purpose of this route is to just reload home route
#   for detect and init camera.
@app.route("/reload")
@login_required
def reload():
    return redirect(url_for("app.home"))


# page -> route robot connect:
# Note:
#   1. This route is used for connecting to ROS Websocket via
#   roslib.js(more specified in js script), also for connect to
#   robot via python socket communication.
#   2. Main purpose is store ip-adress of robot and connect.
#   3. Ajax for start connect.
@app.route("/robot_connect", methods=["POST", "GET"])
@login_required
def robot_connect():
    if request.method == "POST":
        if request.form["value"]:
            message = request.form["value"]
            StoreIP.ip = message

            if message == "127.0.0.1":
                Sim.sim = True

            Robot_info.connect(message)

    return render_template("robot_connect.html")


# ajax -> route play button:
# Note:
#   1. Ajax called route for automate process of hit button play
#   on universal robots polyscope software.
@app.route("/play_button", methods=["POST", "GET"])
@login_required
def play_button():
    if request.method == "POST":
        Robot_info.play_button()

    return render_template("robot_connect.html")


# page -> route disconnect:
# Note:
#   1. in progress
@app.route("/robot_disconnect", methods=["POST", "GET"])
@login_required
def robot_disconnect():
    if request.method == "POST":
        if request.form["value"] == "disconnect":
            StoreIP.ip = "none"
            Sim.sim = False

    return render_template("home.html")


# page -> route menu:
# Note:
#   1. Menu route for menu page.
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html", ip=StoreIP.ip, cam=StoreCam.cam, sim=Sim.sim)


# page -> route control panel:
# Note:
#   1. Control panel menu page.
@app.route("/con_pan")
@login_required
def con_pan():
    return render_template("con_pan.html", pid=StoreID.id)


# page -> route robot control:
# Note:
#   1. Robot control page.
@app.route("/robot_control", methods=["POST", "GET"])
@login_required
def robot_control():
    if request.method == "POST":
        try:
            if request.form["value"] == "cam":
                StreamColorCam.start()
                url = url_for(".video_color")
                return jsonify({"url": url})

            if request.form["value"] == "stop_cam":
                time.sleep(0.5)
                StreamColorCam.stop()
                return jsonify("Stop")

        except RuntimeError:
            return jsonify("Camera is not pluged-in!")

    return render_template("robot_control.html")


# page -> route robot inspection:
# Note:
#   1. This route connect to robot via socket, and feeding
#   defined datas to client.
#   2. Data are yield from data feed route.
#   3. Use ajax for start and stop yielding.
@app.route("/robot_inspection", methods=["POST", "GET"])
@login_required
def robot_inspection():
    if request.method == "POST":
        if request.form["value"] == "data_feed":
            try:
                Robot_info.test_connection()

                url = url_for(".data_feed")
                return jsonify(url)

            except Exception:
                return jsonify("Robot is not connected!")

    return render_template("robot_inspection.html")


# page -> route documentation:
# Note:
#   1. Documentation page.
@app.route("/documentation")
@login_required
def documentation():
    return render_template("documentation.html")


# page -> route authors:
# Note:
#   1. Authors page.
@app.route("/authors")
@login_required
def authors():
    return render_template("authors.html")


# page -> route dash:
# Note:
#   1. After ajax call, do post processing of took point clouds,
#   then return to client, x, y, z coordinates and color of points.
@app.route("/dash", methods=["POST", "GET"])
@login_required
def dash():
    if request.method == "POST":
        # points_x, points_y, points_z, colors = Show_PointCloud.load_pc(Point.point, sim=True)

        points_x, points_y, points_z, colors, point = Show_PointCloud.load_pc(
            Point.point, sim=Sim.sim
        )
        Point.point = point
        print(point)

        return jsonify(
            {
                "x": points_x.tolist(),
                "y": points_y.tolist(),
                "z": points_z.tolist(),
                "c": colors,
                "nx": Point.point[0],
                "ny": Point.point[1],
                "nz": Point.point[2],
            }
        )

    return render_template("dash.html")


# page -> route show camera stream:
# Note:
#   1. Depend of clinet option catch ajax call and stream defined image:
#   color - depth - infra
@app.route("/show_cam_stream", methods=["GET", "POST"])
@login_required
def show_cam_stream():
    if request.method == "POST":
        try:
            if request.form["value"] == "depth_cam":
                StreamCam.start()
                url = url_for(".video_stream_depth")
                return jsonify({"url": url})

            if request.form["value"] == "color_cam":
                StreamCam.start()
                url = url_for(".video_stream_color")
                return jsonify({"url": url})

            if request.form["value"] == "infra_cam":
                StreamCam.start()
                url = url_for(".video_stream_infra")
                return jsonify({"url": url})

            if request.form["value"] == "stop_cam":
                time.sleep(0.5)
                StreamCam.stop()
                return jsonify("Stop")

        except RuntimeError:
            return jsonify("Camera is not pluged-in!")

    return render_template("con_pan_show_cam.html")


# page -> face position:
# Note:
#   1. Take color image and do face ID, if patient selected
#   from database is valid.
@app.route("/faceID", methods=["GET", "POST"])
@login_required
def faceID():
    if request.method == "POST":
        try:
            if request.form["value"] == "stop_reco_cam":
                time.sleep(0.5)
                FaceReco.stop()

            if request.form["value"] == "recognition":

                # database is local sqlite!!!
                if StoreID.id:
                    patient = Patient.query.filter_by(pid=StoreID.id).first()

                    FaceReco.init_patient(
                        patient.photo,
                        str(patient.name + " " + patient.surname),
                    )

                    time.sleep(1)

                    FaceReco.start()

                    url = url_for(".video_feed_facereco")
                    return jsonify({"url": url})

                else:
                    return jsonify("Patient is not init!")

        except RuntimeError:
            return jsonify("Camera is not pluged-in!")

    return render_template("con_pan_faceID.html")


# page -> face position:
# Note:
#   1. Take color image and detec face landmarks.
#   2. Able to control roboto rotation
@app.route("/face_position", methods=["GET", "POST"])
@login_required
def face_position():
    if Validation.val == True:
        if request.method == "POST":
            try:
                if request.form["value"] == "stop_det_cam":
                    time.sleep(0.5)
                    FaceDet.stop()

                if request.form["value"] == "position":
                    FaceDet.start()

                    url = url_for(".video_feed_facedet")
                    return jsonify({"url": url})

            except RuntimeError:
                return jsonify("Camera is not pluged-in!")

        return render_template("con_pan_face_pos.html")

    else:
        return render_template("con_pan.html")


# page -> face scan:
# Note:
#   1. Take color image aligned to depth image
#   and detect center of nostril
#   2. Do 3D reconstruction.
#   3. Do motion to nostril.
@app.route("/face_scan", methods=["GET", "POST"])
@login_required
def face_scan():
    if Validation.val == True:
        if request.method == "POST":
            if request.form["value"] == "scan":
                try:
                    NostrillDet.start()
                    Point.point = NostrillDet.scan_nostrill()
                    
                    print(Point().point)
                    time.sleep(0.5)
                    NostrillDet.stop()

                except RuntimeError:
                    return jsonify("Camera is not pluged-in!")

                if Point.point is None:
                    return jsonify("once_again")

                else:
                    _, _, _, _, point = Show_PointCloud.load_pc(
                        Point.point, sim=Sim.sim
                    )
                    print(Sim.sim)
                    Point2.point = point
                    print(Point2().point)

                    return jsonify("ok")

            if request.form["value"] == "test":
                if Point2.point is not None:
                    return jsonify(
                        {
                            "sim": Sim.sim,
                            "point": [
                                Point2.point[0],
                                Point2.point[1],
                                Point2.point[2],
                            ],
                        }
                    )

                else:
                    return jsonify("nok")

        return render_template("con_pan_face_scan.html", sim=Sim.sim)

    else:
        return render_template("con_pan.html")


# page -> route patient data:
# Note:
#   1. After stop qr detector find patient in patients database by personal identification number,
#   and show all datas from patients database include encoded image
#   2. Closely related to patient menu
#   3. Same render page in auth blueprint part.
@app.route("/store_data_qr", methods=["GET", "POST"])
@login_required
def store_data_qr():
    if request.method == "POST":
        if request.form["value"] == "store_qr_cam":
            data = ReadQR.output_data()

            if data:
                data = data[0][0].decode("utf-8")
                StoreID.id = data

    return render_template("patient_menu.html", cam=StoreCam.cam)


# route -> video stream color QR:
# Note:
#   1. Stream color image with qr code detector.
#   2. By finded PID render patient_data
@app.route("/patient_data_qr")
@login_required
def patient_data_qr():
    data = StoreID.id
    patient = Patient.query.filter_by(pid=data).first()

    if patient:
        image = b64encode(patient.photo).decode("utf-8")
        return render_template(
            "patient_data.html",
            patient=patient,
            obj=patient.photo,
            image=image,
        )

    else:
        return render_template("patients_searched.html", patient=None)


# page -> route patient menu:
# Note:
#   1. In this route we can start QR detector from color image camera, or client may redirect to
#   patient_find route in auth blueprint.
#   2. Color image is yield from video_stream_QR route.
#   3. Closely related to patient data qr route
@app.route("/patient_menu", methods=["GET", "POST"])
@login_required
def patient_menu():
    if request.method == "POST":
        try:
            if request.form["value"] == "QR_detection":
                ReadQR.start()
                url = url_for(".video_stream_QR")
                return jsonify({"url": url})

            if request.form["value"] == "stop_qr_cam":
                ReadQR.stop()

        except RuntimeError:
            return jsonify("Camera is not pluged-in!")

    return render_template("patient_menu.html", cam=StoreCam.cam)


# yield -> route video stream QR detector:
# Note:
#   1. Stream color image with qr code detector.
@app.route("/video_stream_QR")
@login_required
def video_stream_QR():
    def generate():
        while 1:
            try:
                frame = ReadQR.QR_code_reader()

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route video stream face recognition(FaceID):
# Note:
#   1. Stream color image with face recognition and store validation.
@app.route("/video_feed_facereco")
@login_required
def video_feed_facereco():
    def generate():
        while 1:
            try:
                frame = FaceReco.recognize()
                Validation.val = FaceReco.get_val()
                # print(Validation.val)

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route video stream face detector:
# Note:
#   1. Stream color image with face detection of position and store validation.
@app.route("/video_feed_facedet")
@login_required
def video_feed_facedet():
    def generate():
        while 1:
            try:
                frame = FaceDet.set_position()
                Validation.val = FaceDet.get_val()

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route video stream color:
# Note:
#   1. Stream pure color image.
#   2. If you change switch, you just switch to another mode streaming.
@app.route("/video_stream_color")
@login_required
def video_stream_color():
    # idea of secure this type of routes is use Token
    # if Token.token == True:
    def generate():
        while 1:
            try:
                # start_time = time.time()
                frame = StreamCam.get_frame(switch=0)
                # print("FPS: ", 1.0 / (time.time() - start_time))

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

    # else:
    #    return redirect(url_for('app.home'))


# yield -> route video stream color:
# Note:
#   1. Stream pure color image to control robot route.
@app.route("/video_color")
@login_required
def video_color():
    def generate():
        while 1:
            try:
                # start_time = time.time()
                frame = StreamColorCam.get_frame()
                # print("FPS: ", 1.0 / (time.time() - start_time))

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route video stream depth:
# Note:
#   1. Stream pure depth image.
#   2. If you change switch, you just switch to another mode streaming.
@app.route("/video_stream_depth")
@login_required
def video_stream_depth():
    def generate():
        while 1:
            try:
                frame = StreamCam.get_frame(switch=1)

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route video stream infra:
# Note:
#   1. Stream pure infra image.
#   2. If you change switch, you just switch to another mode streaming.
@app.route("/video_stream_infra")
@login_required
def video_stream_infra():
    def generate():
        while 1:
            try:
                frame = StreamCam.get_frame(switch=2)

            except AttributeError:
                break

            except RuntimeError:
                break

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# yield -> route data feed from robot:
# Note:
#   1. Stream data for charts into client.
@app.route("/data_feed")
@login_required
def data_feed():
    if request.headers.get("accept") == "text/event-stream":

        def gen_data():
            while 1:
                try:
                    data = Robot_info.get_data()
                    yield ("data: {}\n\n").format(data)

                except Exception:
                    break

        return Response(gen_data(), content_type="text/event-stream")

    return render_template("404.html"), 404
