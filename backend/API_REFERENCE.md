# API Reference - Space Station Management System

Complete API endpoint reference with request/response examples.

---

## Base URL

**Local Development:** `http://localhost:8000`  
**Production:** `https://your-app.vercel.app`

---

## Table of Contents

1. [Health & Info](#health--info)
2. [Authentication](#authentication)
3. [Missions](#missions)
4. [Experiments](#experiments)
5. [Error Responses](#error-responses)

---

## Health & Info

### Get API Info

Returns basic information about the API.

**Endpoint:** `GET /`

**Response:** `200 OK`
```json
{
  "message": "Space Station Management System API",
  "status": "operational",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### Health Check

Checks API and database connectivity.

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "api": "healthy",
  "database": "connected"
}
```

---

## Authentication

### Login

Authenticate crew member and retrieve their details.

**Endpoint:** `POST /login`

**Request Body:**
```json
{
  "crew_id": 1,
  "password": "password123"
}
```

**Success Response:** `200 OK`
```json
{
  "crew_id": 1,
  "name": "John Mitchell",
  "role": "Commander",
  "nationality": "USA",
  "message": "Login successful"
}
```

**Error Response:** `401 Unauthorized`
```json
{
  "detail": "Invalid crew ID or password"
}
```

**Error Response:** `500 Internal Server Error`
```json
{
  "detail": "An error occurred during login: [error message]"
}
```

---

## Missions

### Get All Missions

Retrieve all missions with crew member names.

**Endpoint:** `GET /missions`

**Response:** `200 OK`
```json
[
  {
    "mission_id": 1,
    "name": "ISS Maintenance Alpha",
    "purpose": "Routine maintenance and inspection of ISS solar panels",
    "crew_id": 1,
    "crew_name": "John Mitchell"
  },
  {
    "mission_id": 2,
    "name": "Mars Sample Analysis",
    "purpose": "Analyze soil samples from Mars returned by previous missions",
    "crew_id": 4,
    "crew_name": "Maria Santos"
  }
]
```

**Empty Response:** `200 OK`
```json
[]
```

---

### Create Mission

Create a new mission.

**Endpoint:** `POST /missions`

**Request Body:**
```json
{
  "name": "Lunar Base Setup",
  "purpose": "Initial construction of lunar base modules",
  "crew_id": 5
}
```

**Request Body Fields:**
- `name` (string, required): Mission name (1-255 characters)
- `purpose` (string, required): Mission purpose (1-500 characters)
- `crew_id` (integer, required): Assigned crew member ID

**Success Response:** `201 Created`
```json
{
  "mission_id": 6,
  "name": "Lunar Base Setup",
  "purpose": "Initial construction of lunar base modules",
  "crew_id": 5,
  "message": "Mission created successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Crew member with ID 99 not found"
}
```

**Error Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Update Mission

Update an existing mission (partial updates supported).

**Endpoint:** `PUT /missions/{mission_id}`

**Path Parameters:**
- `mission_id` (integer, required): Mission ID to update

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Mission Name",
  "purpose": "Updated mission purpose",
  "crew_id": 2
}
```

**Request Body Fields:**
- `name` (string, optional): New mission name
- `purpose` (string, optional): New mission purpose
- `crew_id` (integer, optional): New assigned crew member ID

**Success Response:** `200 OK`
```json
{
  "message": "Mission 1 updated successfully"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "detail": "No fields to update"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Mission with ID 999 not found"
}
```

---

### Delete Mission

Delete a mission.

**Endpoint:** `DELETE /missions/{mission_id}`

**Path Parameters:**
- `mission_id` (integer, required): Mission ID to delete

**Success Response:** `200 OK`
```json
{
  "message": "Mission 1 deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Mission with ID 999 not found"
}
```

---

## Experiments

### Get All Experiments

Retrieve all experiments with crew member names.

**Endpoint:** `GET /experiments`

**Response:** `200 OK`
```json
[
  {
    "experiment_id": 1,
    "title": "Plant Growth in Microgravity",
    "status": "In Progress",
    "crew_id": 4,
    "crew_name": "Maria Santos"
  },
  {
    "experiment_id": 2,
    "title": "Protein Crystal Formation",
    "status": "Completed",
    "crew_id": 4,
    "crew_name": "Maria Santos"
  }
]
```

**Empty Response:** `200 OK`
```json
[]
```

---

### Create Experiment

Create a new experiment.

**Endpoint:** `POST /experiments`

**Request Body:**
```json
{
  "title": "Zero-G Manufacturing Test",
  "status": "Planned",
  "crew_id": 3
}
```

**Request Body Fields:**
- `title` (string, required): Experiment title (1-255 characters)
- `status` (string, required): Experiment status (1-100 characters)
- `crew_id` (integer, required): Assigned crew member ID

**Success Response:** `201 Created`
```json
{
  "experiment_id": 8,
  "title": "Zero-G Manufacturing Test",
  "status": "Planned",
  "crew_id": 3,
  "message": "Experiment created successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Crew member with ID 99 not found"
}
```

---

### Update Experiment

Update an existing experiment (partial updates supported).

**Endpoint:** `PUT /experiments/{experiment_id}`

**Path Parameters:**
- `experiment_id` (integer, required): Experiment ID to update

**Request Body:** (all fields optional)
```json
{
  "title": "Updated Experiment Title",
  "status": "Completed",
  "crew_id": 2
}
```

**Request Body Fields:**
- `title` (string, optional): New experiment title
- `status` (string, optional): New experiment status
- `crew_id` (integer, optional): New assigned crew member ID

**Success Response:** `200 OK`
```json
{
  "message": "Experiment 1 updated successfully"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "detail": "No fields to update"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Experiment with ID 999 not found"
}
```

---

### Delete Experiment

Delete an experiment.

**Endpoint:** `DELETE /experiments/{experiment_id}`

**Path Parameters:**
- `experiment_id` (integer, required): Experiment ID to delete

**Success Response:** `200 OK`
```json
{
  "message": "Experiment 1 deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Experiment with ID 999 not found"
}
```

---

## Error Responses

### Common Error Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request - invalid input |
| 401 | Unauthorized - invalid credentials |
| 404 | Not found - resource doesn't exist |
| 422 | Unprocessable entity - validation error |
| 500 | Internal server error |

### Error Response Format

All errors return a JSON object with a `detail` field:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Errors (422)

Pydantic validation errors include detailed field information:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

---

## Common Status Codes by Endpoint

### Authentication

| Endpoint | Success | Error Codes |
|----------|---------|-------------|
| POST /login | 200 | 401, 500 |

### Missions

| Endpoint | Success | Error Codes |
|----------|---------|-------------|
| GET /missions | 200 | 500 |
| POST /missions | 201 | 400, 404, 422, 500 |
| PUT /missions/{id} | 200 | 400, 404, 500 |
| DELETE /missions/{id} | 200 | 404, 500 |

### Experiments

| Endpoint | Success | Error Codes |
|----------|---------|-------------|
| GET /experiments | 200 | 500 |
| POST /experiments | 201 | 400, 404, 422, 500 |
| PUT /experiments/{id} | 200 | 400, 404, 500 |
| DELETE /experiments/{id} | 200 | 404, 500 |

---

## Request Headers

All POST and PUT requests require:

```
Content-Type: application/json
```

---

## Response Headers

All responses include:

```
Content-Type: application/json
Access-Control-Allow-Origin: * (or configured domain)
```

---

## CORS

The API supports CORS for all origins in development. In production, update CORS settings to allow only your frontend domain.

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS  
**Allowed Headers:** All  
**Credentials:** Supported  

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

---

## Pagination

Currently not implemented. All GET endpoints return all records. Consider implementing pagination for large datasets.

---

## Sorting & Filtering

Currently not implemented. Results are ordered by ID descending for missions and experiments.

---

## Interactive Documentation

Access interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide:
- Interactive API testing
- Request/response examples
- Schema definitions
- Try-it-out functionality

---

## Example Workflows

### Complete Mission Workflow

1. **Login as crew member**
   ```bash
   POST /login
   {"crew_id": 1, "password": "password123"}
   ```

2. **View all missions**
   ```bash
   GET /missions
   ```

3. **Create new mission**
   ```bash
   POST /missions
   {"name": "New Mission", "purpose": "Test", "crew_id": 1}
   ```

4. **Update mission**
   ```bash
   PUT /missions/1
   {"status": "In Progress"}
   ```

5. **Delete mission**
   ```bash
   DELETE /missions/1
   ```

---

## Database Relations

### Mission → Crew
- Each mission must have a valid crew_id
- Deleting a crew member cascades to their missions

### Experiment → Crew
- Each experiment must have a valid crew_id
- Deleting a crew member cascades to their experiments

---

## Notes

- All timestamps are in UTC
- IDs are auto-incrementing integers
- Password comparison is case-sensitive
- Foreign key constraints are enforced
- Transactions are atomic (rollback on error)

---

**For more information, see:**
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
