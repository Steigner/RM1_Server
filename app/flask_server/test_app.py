import unittest
from app import create_app

class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LOGIN_DISABLED'] = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_root(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertAlmostEqual(response.status_code, 200)
    
    def sign_in(self, email, password):
        return self.client.post('/sign_in', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def sign_out(self):
        return self.client.get('/sign_out', follow_redirects=True)

    def test_user_signin(self):
        # this will be changed by test@test.com and test
        email = 'email@email.com'
        password = 'heslo'
        
        response = self.sign_in(email, password)

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes'])

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(flash_message['message'], 'user sign in')
        self.assertIsNotNone(flash_message, session['_flashes'])

    def test_user_signin(self):
        # this will be changed by test@test.com and test
        email = 'supervisor@email.com'
        password = 'heslo'
        
        response = self.sign_in(email, password)

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes'])

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(flash_message['message'], 'admin sign in')
        self.assertIsNotNone(flash_message, session['_flashes'])
    
    def test_signout(self):
        response = self.sign_out()
        self.assertEqual(response.status_code, 200)

    def test_patient_find(self):
        pass
    
    def test_robot_connect(self):
        pass

    def test_robot_control(self):
        response = self.client.get('/robot_control', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_robot_inspection(self):
        response = self.client.get('/robot_inspection', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_documentation(self):
        response = self.client.get('/documentation', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/authors', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_camera(self):
        # TODO -> exactly same!!!
        response = self.client.get('/show_cam_stream', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        self.client.post('/show_cam_stream', data={'value': 'color_cam'})
        self.assertEqual(response.status_code, 200)

        self.client.post('/show_cam_stream', data={'value': 'depth_cam'})
        self.assertEqual(response.status_code, 200)

        self.client.post('/show_cam_stream', data={'value': 'infra_cam'})
        self.assertEqual(response.status_code, 200)

        self.client.post('/show_cam_stream', data={'value': 'stop_cam'})
        self.assertEqual(response.status_code, 200)

        self.client.post('/video_feed_facedet')
        self.assertEqual(response.status_code, 200)
        
        """
        response = self.client.get('/face_position', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/faceID', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        """

        # exception for no device connected !!
        # response = self.client.get('/face_scan', follow_redirects=True)
        # self.assertEqual(response.status_code, 200)

    def ip_adress(self):
        response = self.client.get('/ip_adress', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_dash(self):
        response = self.client.get('/dash', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()