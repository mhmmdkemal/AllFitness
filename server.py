from flask_app import app
from flask_app.controllers import users, dojoMembers, workouts # ALWAYS IMPORT YOUR CONTROLLERS!!!

if __name__ == "__main__":
    app.run(debug=True) #host='0.0.0.0', port= 5001)
