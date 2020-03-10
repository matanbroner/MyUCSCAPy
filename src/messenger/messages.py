from ..assets.utils import strip_ws
def course_open_message(course_name, course_url, occupied_spots, total_spots):
    open_spots = total_spots - occupied_spots
    # message = "\nCourse \"{}\"\n{} of {} spots now open!\nCourse URL: {}".format(course_name, open_spots, total_spots, course_url)
    html = """
    <div>
    Course \"{}\"
    <br/>
    {} of {} spots now open!
    <br/>
    Course URL: {}
    </div>
    """.format(course_name, open_spots, total_spots, course_url)
    return html.strip()

def test_message():
    message = """\
    <html>
    <body>
    <div>
    Test Message!<br/>
    <a href="google.com">Click Here</a> to navigate to the Google.
    </div>
    </body>
    </html>
    """
    return message