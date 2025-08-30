#!/usr/bin/env bash
set -euo pipefail

# Boot the Flask application in the background.  The PID is captured so
# we can terminate the server once the checks have completed.  The
# development server binds to port 5000 by default as configured in
# ``app/__main__.py``.
python3 -m app & PID=$!

# Give the server a moment to start up before making HTTP requests.
sleep 2

# Check that the login route renders successfully.  ``curl -sf``
# suppresses progress output and treats non‑success status codes as
# errors.
curl -sf http://localhost:5000/login > /dev/null
echo "Login route OK"

# Create a dummy G‑Code file and POST it to the upload endpoint.  The
# response should be valid JSON.  We write a temporary file into the
# current working directory.
touch temp.gcode && echo ";dummy" > temp.gcode
curl -sf -F "file=@temp.gcode" http://localhost:5000/gcode/upload | jq .

echo "G‑Code upload OK"

# Create a dummy STL file and POST it to the thumbnail upload endpoint.
# The endpoint may return either a 201 Created or a 302 Found status.
touch temp.stl && echo "solid" > temp.stl
CODE=$(curl -s -o /dev/null -w "%{http_code}" -F "file=@temp.stl" http://localhost:5000/thumbs/upload)
[[ "$CODE" == "201" || "$CODE" == "302" ]] && echo "Thumb upload OK" || (echo "Thumb upload failed" && kill $PID && exit 1)

# Clean up the server and temporary files.
kill $PID
rm temp.gcode temp.stl

echo "🟢 Scaffold passes basic smoke test"