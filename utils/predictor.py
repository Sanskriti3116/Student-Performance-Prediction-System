import joblib

# Load trained ML model
model = joblib.load("models/student_model.pkl")


def mood_to_number(mood):

    if mood == "Good":
        return 2

    elif mood == "Average":
        return 1

    else:
        return 0


def predict_performance(
    study_hours,
    attendance_percent,
    sleep_hours,
    mood
):

    mood_value = mood_to_number(mood)

    prediction = model.predict([[
        study_hours,
        attendance_percent,
        sleep_hours,
        mood_value
    ]])

    return round(float(prediction[0]), 2)