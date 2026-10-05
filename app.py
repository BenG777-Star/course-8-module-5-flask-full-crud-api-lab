from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class required by the lab design
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory data store seeded with records
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]
next_id = 3


# Helper function to easily locate an event by its ID
def find_event_by_id(event_id):
    return next((e for e in events if e.id == event_id), None)


# Task 3.1: POST /events - Create a new event from JSON input
@app.route('/events', methods=['POST'])
def create_event():
    global next_id
    data = request.get_json()

    # Input validation: Check for missing payload or fields
    if not data or 'title' not in data:
        return jsonify({"error": "Bad Request", "message": "Missing required field: 'title'"}), 400

    new_event = Event(id=next_id, title=str(data['title']))
    events.append(new_event)
    next_id += 1

    return jsonify(new_event.to_dict()), 201


# Task 3.2: PATCH /events/<id> - Update the title of an event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def patch_event(event_id):
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Bad Request", "message": "Missing required field: 'title'"}), 400

    event = find_event_by_id(event_id)
    
    # Validation: Return 404 if the item index doesn't exist
    if not event:
        return jsonify({"error": "Not Found", "message": f"Event with ID {event_id} not found"}), 404

    event.title = str(data['title'])
    return jsonify(event.to_dict()), 200


# Task 3.3: DELETE /events/<id> - Remove an event from the list (Returns 204 No Content)
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    event = find_event_by_id(event_id)

    if not event:
        return jsonify({"error": "Not Found", "message": f"Event with ID {event_id} not found"}), 404

    events = [e for e in events if e.id != event_id]
    
    # Empty string with a 204 status satisfies the test_delete_event assertion
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
