# Udatracker Order Management System

## Reflection

- **Design decision — fail-fast validation:** In `OrderTracker`, I chose to validate inputs (empty IDs, invalid quantities, invalid statuses) before making any storage calls. This ordering means obviously bad requests are rejected immediately without wasting a read from storage, which would matter more in a real system with a database.

- **Testing insight — mocks don't enforce contracts:** Early on, I passed five separate arguments to `save_order` in my implementation, and the unit tests passed because `Mock()` accepts any arguments. It wasn't until I thought about how `InMemoryStorage.save_order` actually works (expecting `order_id` and a dict) that I realized the mismatch. This taught me that mocks verify behavior, not compatibility — integration tests are what catch contract mismatches.

- **Design decision — optional status in the API:** The `status` field in the POST endpoint is optional, defaulting to `"pending"`. I initially hardcoded `data['status']` which broke every test that didn't send a status. Using `data.get('status', 'pending')` solved it and aligned the API layer with the business logic default.

- **Next step:** I would add a `DELETE /api/orders/<order_id>` endpoint and persistent storage (e.g., SQLite) so that orders survive server restarts.

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```
