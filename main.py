from flask import Flask, render_template, request
import fitparse
import gpxpy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request contains a file
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']

        # Check the file extension
        if file.filename.endswith('.fit'):
            data = parse_fit(file)
        elif file.filename.endswith('.tcx'):
            data = parse_tcx(file)
        elif file.filename.endswith('.gpx'):
            data = parse_gpx(file)
        else:
            return 'Invalid file format. Only FIT, TCX, and GPX files are supported.', 400

        return render_template('file_data.html', data=data)

    return render_template('upload.html')

def parse_fit(file):
    fitfile = fitparse.FitFile(file)
    """
    # Iterate over the messages and print their details
    for message in fitfile:
        print(message.name)
        for field in message:
            print("-- "+field.name, field.value)
    """
    data = []
    for record in fitfile.get_messages('file_id'):
        r = {}
        for field in record:
            print(field.name + "-- "+str(field.value))
            r[field.name] = field.value
        data.append(r)
    # Print each item in the data list
    #for item in data:
    #    print(item+"--")
    return data

def parse_tcx(file):
    tcx = gpxpy.parse(file)
    data = []
    for track in tcx.tracks:
        for segment in track.segments:
            for point in segment.points:
                r = {}
                r['latitude'] = point.latitude
                r['longitude'] = point.longitude
                r['elevation'] = point.elevation
                # Add any additional data you want to extract from TCX files
                data.append(r)
    return data

def parse_gpx(file):
    gpx = gpxpy.parse(file)
    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                r = {}
                r['latitude'] = point.latitude
                r['longitude'] = point.longitude
                r['elevation'] = point.elevation
                # Add any additional data you want to extract from GPX files
                data.append(r)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
