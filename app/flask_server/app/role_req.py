# library -> standard python libary - wraps
from functools import wraps

# library -> flask login - get currenct user fresh logged in
from flask_login import current_user

# public function:
#   input: role
#   return: wrap
# Note: own wrapper which provide protection before non-admin user to log in admin layer.
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "Admin":
            return f(*args, **kwargs)
        else:
            return "<h1>You need to be an admin to view this page.<h1>"

    return wrap
