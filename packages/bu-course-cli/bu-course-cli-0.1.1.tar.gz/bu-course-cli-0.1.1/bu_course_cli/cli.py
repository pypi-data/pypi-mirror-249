import requests
import argparse
import json
import re

def standardize_course_code(course_code):
    # Standardize course code to match the format in the data source
    course_code = course_code.upper()  # Convert to uppercase
    parts = course_code.split()
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"  # Ensure the correct format with a space
    return course_code  # Return as-is if format is not as expected

def list_courses(base_url):
    response = requests.get(f"{base_url}/courses")
    if response.status_code == 200:
        courses = response.json()
        for course in courses:
            print(f"{course['course_code']}: {course['course_title']}")
    else:
        print("Error: Unable to retrieve courses.")

def get_course(base_url, course_code):
    course_code = standardize_course_code(course_code)
    response = requests.get(f"{base_url}/courses/{course_code}")
    if response.status_code == 200:
        course = response.json()
        print(json.dumps(course, indent=2))
    else:
        print("Error: Course not found.")

def search_courses(base_url, query):
    response = requests.get(f"{base_url}/courses/search", params={'query': query})
    if response.status_code == 200:
        courses = response.json()
        for course in courses:
            print(f"{course['course_code']}: {course['course_title']}")
    else:
        print("Error: Unable to perform search.")

def compare_courses(base_url, course_codes):
    course_codes = [standardize_course_code(code) for code in course_codes.split(',')]
    courses_to_compare = course_codes.split(',')
    course_details = []

    for code in courses_to_compare:
        response = requests.get(f"{base_url}/courses/{code.strip()}")
        if response.status_code == 200:
            course_details.append(response.json())
        else:
            print(f"Error: Course with code {code} not found.")
            return

    for detail in course_details:
        print(f"Course Code: {detail['course_code']}")
        print(f"Course Title: {detail['course_title']}")
        print(f"Description: {detail['description']}\n")

    if len(course_details) == 2:
        # Here you could add more detailed comparison logic if needed
        print("Comparison Complete.")

def format_course_code(prerequisites):
    # First, insert a space between the department code and course number (e.g., "CDS" and "DS121")
    formatted_prerequisites = re.sub(r'([a-zA-Z]{3})([a-zA-Z]+\d+)', r'\1 \2', prerequisites)
    # Next, insert a space within concatenated course codes (e.g., "DS" and "121")
    formatted_prerequisites = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', formatted_prerequisites)
    return formatted_prerequisites

def get_prerequisites(base_url, course_code):
    course_code = standardize_course_code(course_code)
    response = requests.get(f"{base_url}/courses/{course_code}")
    if response.status_code == 200:
        course = response.json()
        prerequisites = course.get('prerequisites')
        if not prerequisites or prerequisites == "=":
            print("N/A")
        else:
            print(format_course_code(prerequisites))
    else:
        print("Error: Course not found.")

def main():
    parser = argparse.ArgumentParser(description="BU Courses CLI")
    parser.add_argument('--list', help="List all courses", action="store_true")
    parser.add_argument('--get', help="Get a specific course by code", type=str)
    parser.add_argument('--search', help="Search courses by keyword", type=str)
    parser.add_argument('--compare', help="Compare two courses by code, separated by a comma", type=str)
    parser.add_argument('--prereqs', help="Get prerequisites for a specific course by code", type=str)
    parser.add_argument('--base-url', help="Base URL for the courses API", type=str, default="https://bu-course-cli-410302.ue.r.appspot.com")

    args = parser.parse_args()

    if args.list:
        list_courses(args.base_url)
    elif args.get:
        get_course(args.base_url, args.get)
    elif args.search:
        search_courses(args.base_url, args.search)
    elif args.compare:
        compare_courses(args.base_url, args.compare)
    elif args.prereqs:
        get_prerequisites(args.base_url, args.prereqs)

if __name__ == "__main__":
    main()