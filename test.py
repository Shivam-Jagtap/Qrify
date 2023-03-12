# import pyqrcode
# import png

# ## generating qr code
# # String which represents the QR code
# s = "www.geeksforgeeks.org"

# # Generate QR code
# url = pyqrcode.create(s)

# # Create and save the svg file naming "myqr.svg"
# url.svg("myqr.svg", scale = 8)

# # Create and save the png file naming "myqr.png"
# url.png('myqr.png', scale = 6)


# ## rendering image from template/static/qrPhotos into webpage
# @app.route('/static/qrPhotos/<filename>')
# def send_file(filename):
#     return send_from_directory(os.path.join("templates", "static", "qrPhotos"), filename)

# @app.route('/')
# def index():
#     image_filename = "dwight.jpeg"
#     image_path = url_for("send_file", filename=image_filename)
#     return render_template("index.html", image=image_path)

