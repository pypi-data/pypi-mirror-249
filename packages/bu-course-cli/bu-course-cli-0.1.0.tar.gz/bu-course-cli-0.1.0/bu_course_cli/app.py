from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load course data from the provided JSON file
with open('full_list.json', 'r') as f:
    courses = json.load(f)

@app.route('/', methods=['GET'])
def index():
    # Provide instructions for using the API
    return jsonify({
        "message": "Welcome to the BU Courses API.",
        "usage": {
            "list_courses": "GET /courses",
            "get_course": "GET /courses/<course_code>",
            "search_courses": "GET /courses/search?query=<search_query>"
        },
        "example": {
            "list_courses": request.host_url + "courses",
            "get_course": request.host_url + "courses/CDS DS 100",
            "search_courses": request.host_url + "courses/search?query=data"
        }
    })

@app.route('/courses', methods=['GET'])
@app.route('/courses/', methods=['GET'])  # Add this line to handle the trailing slash
def list_courses():
    # Return a list of course codes and titles
    return jsonify([{ "course_code": course["course_code"], "course_title": course["course_title"] } for course in courses])

@app.route('/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    # Find the course by course_code
    course = next((course for course in courses if course['course_code'] == course_code), None)
    return jsonify(course) if course else ('Course not found', 404)

# Let's also add a search functionality
@app.route('/courses/search', methods=['GET'])
def search_courses():
    query = request.args.get('query', '').lower()
    filtered_courses = [course for course in courses if query in course["course_title"].lower()]
    return jsonify(filtered_courses)

if __name__ == '__main__':
    app.run(debug=True)
