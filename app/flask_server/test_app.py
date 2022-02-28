# library -> unit testing framework
import unittest

# script -> import create_app function
from app import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["LOGIN_DISABLED"] = True
        self.client = app.test_client()

    def test_root(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertAlmostEqual(response.status_code, 200)

    def sign_in(self, email, password):
        return self.client.post(
            "/sign_in",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    def sign_out(self):
        return self.client.get("/sign_out", follow_redirects=True)

    def test_user_signin(self):
        email = "email@email.com"
        password = "heslo"

        response = self.sign_in(email, password)

        with self.client.session_transaction() as session:
            flash_message = dict(session["_flashes"])

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(flash_message["message"], "user sign in")
        self.assertIsNotNone(flash_message, session["_flashes"])

    def test_signout(self):
        response = self.sign_out()
        self.assertEqual(response.status_code, 200)

    def test_robot_connect_disconnect(self):
        response = self.client.get("/robot_connect", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/robot_connect", data={"value": "127.0.0.1"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/play_button", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/robot_disconnect", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/robot_disconnect", data={"value": "disconnect"})
        self.assertEqual(response.status_code, 200)

    def test_robot_control(self):
        response = self.client.get("/robot_control", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/robot_control", data={"value": "cam"})
        self.assertEqual(response.status_code, 200)

    def test_robot_inspection(self):
        response = self.client.get("/robot_inspection", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/robot_inspection", data={"value": "data_feed"}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_documentation(self):
        response = self.client.get("/documentation", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/authors", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_camera(self):
        response = self.client.get("/con_pan", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/show_cam_stream", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        self.client.post("/show_cam_stream", data={"value": "color_cam"})
        self.assertEqual(response.status_code, 200)

        self.client.post("/show_cam_stream", data={"value": "depth_cam"})
        self.assertEqual(response.status_code, 200)

        self.client.post("/show_cam_stream", data={"value": "infra_cam"})
        self.assertEqual(response.status_code, 200)

        self.client.post("/show_cam_stream", data={"value": "stop_cam"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/face_position", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/face_position", data={"value": "position"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/faceID", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/faceID", data={"value": "recognition"})
        self.assertEqual(response.status_code, 200)

    def ip_adress(self):
        response = self.client.get("/ip_adress", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_face_scan(self):
        response = self.client.get("/face_scan", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/face_scan", data={"value": "scan"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/face_scan", data={"value": "test"})
        self.assertEqual(response.status_code, 200)

    def test_data_qr(self):
        response = self.client.get("/store_data_qr", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/store_data_qr", data={"value": "store_qr_cam"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/patient_data_qr", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_patient_menu(self):
        response = self.client.get("/patient_menu", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/patient_menu", data={"value": "QR_detection"})
        self.assertEqual(response.status_code, 200)

    def test_dash(self):
        response = self.client.get("/dash", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_patient_search(self):
        response = self.client.get("/patients_searched", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/patient_data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/patient_data_f", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/patient_gen", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pdf(self):
        response = self.client.get("/download", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get("/home", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/reload", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_done(self):
        response = self.client.get("/done", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/done", data={"value": "done"})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
