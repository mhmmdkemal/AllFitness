from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

class Workout:
    db_name = "all_fitness_schema"

    def __init__(self, workout):
        self.id = workout["id"]
        self.experience = workout["experience"]
        self.goals = workout["goals"]
        self.days = workout["days"]
        self.routine = workout["routine"]
        self.created_at = workout["created_at"]
        self.updated_at = workout["updated_at"]
        self.user = None


    @classmethod
    def create_workout(cls, workout_dict):
        if not cls.is_valid(workout_dict):
            return False

        query = """INSERT INTO workouts (experience ,goals ,days, routine, user_id) VALUES (%(experience)s, %(goals)s, %(days)s, %(routine)s, %(user_id)s);"""

        workout = connectToMySQL(cls.db_name).query_db(query, workout_dict)
        print("This is the workout id!!!!!", workout_dict)
        # workout = cls.get_workout_by_id(workout_id)
        # print(workout)

        return workout

    @classmethod
    def get_workout_by_id(cls, workout_dict):
        print(f"get workout by id{workout_dict}")
        data =  {"id" : workout_dict}
        query  =""" SELECT * FROM workouts
        JOIN users on users.id = workouts.user_id
        WHERE workouts.id = %(id)s;"""

        result = connectToMySQL(cls.db_name).query_db(query, data)
        print("result of query:")
        print(result)
        result = result[0]
        print(result)
        workout = cls(result)

        workout.user = user.User(
            {
                "id": result["user_id"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "email": result ["email"],
                "password": False,
                "account_type": result["account_type"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
            }
        )
        return workout

    @classmethod
    def delete_routine_by_id(cls, workout_id):

        data={"id": workout_id}
        query = "DELETE from workouts WHERE id = %(id)s;"
        connectToMySQL(cls.db_name).query_db(query, data)

        return workout_id

    @classmethod
    def update_workout(cls, workout_dict, session_id):
        # print(workout_dict["id"])
        workout = cls.get_workout_by_id(workout_dict["id"])
        # if workout.user.id != session_id:
        #     flash("You must be the creator to update this routine ")
        #     return False

        # if not cls.is_valid(workout_dict):
        #     return False

        query = """UPDATE workouts
                    SET experience = %(experience)s, goals = %(goals)s, days = %(days)s, routine= %(routine)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(cls.db_name).query_db(query, workout_dict)
        workout = cls.get_workout_by_id(workout_dict["id"])

        return workout

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM workouts
        JOIN users
        ON workouts.user_id = users.id ;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        #if we dont find any workoutss return an empty list
        if len(results)==0:
            return []
        else:
            all_workouts_object = [] # this will hold Trails
            for workouts_dictionary in results:

                #create the workouts
                workouts_obj = cls(workouts_dictionary)
                # Grab the user object
                user_dictionary = {
                    "id": workouts_dictionary["users.id"],
                    "first_name": workouts_dictionary["first_name"],
                    "last_name": workouts_dictionary["last_name"],
                    "email": workouts_dictionary["email"],
                    "password": workouts_dictionary["password"],
                    "account_type": workouts_dictionary["account_type"],
                    "created_at": workouts_dictionary["users.created_at"],
                    "updated_at": workouts_dictionary["users.updated_at"],
                }

                # create user object
                user_obj = user.User(user_dictionary)
                # Link this user to this workoutsi
                workouts_obj.user = user_obj
                #add this workouts to the list of all workouts objects
                all_workouts_object.append(workouts_obj)
            return all_workouts_object

    @staticmethod
    def is_valid(workout_dict):
        valid = True
        if len(workout_dict["experience"]) < 4:
            flash("Experience field should be at least 5 characters!.")
            valid = False
        if len(workout_dict["goals"]) < 3 :
            flash("Body Type Goals field should be at least 3 characters!")
            valid = False
        if len(workout_dict["routine"]) < 15:
            flash("Enter your routine with description to help others!")
            valid = False

        return valid
