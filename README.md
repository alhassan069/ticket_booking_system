# 🎫 Ticket Booking System

A modern, full-stack ticket booking management system built with **FastAPI** and **SQLAlchemy**. This application provides a complete solution for managing events, venues, ticket types, and bookings with robust database relationships and RESTful API endpoints.

## ✨ Features

### 🎭 Event Management
- Create and manage events with detailed information
- Track event bookings and revenue
- View available tickets for each event
- Event scheduling with start and end times

### 🏟️ Venue Management
- Manage venues with capacity tracking
- Location-based venue organization
- View all events at specific venues
- Capacity and occupancy statistics

### 🎟️ Ticket Type System
- Multiple ticket categories (VIP, Standard, Economy)
- Flexible pricing structure
- Track bookings by ticket type
- Revenue analysis per ticket category

### 📅 Booking System
- Create bookings with event, venue, and ticket type relationships
- Booking status management (pending, confirmed, cancelled)
- Unique confirmation codes for each booking
- Real-time availability tracking

### 📊 Advanced Analytics
- Revenue reporting by event, venue, and time period
- Venue occupancy statistics
- Booking search and filtering
- Comprehensive booking statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ticket_booking_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Web Interface: http://localhost:8000
   - Alternative API docs: http://localhost:8000/redoc

## 📚 API Documentation

### Events Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/events` | Create a new event |
| `GET` | `/events` | Get all events |
| `GET` | `/events/{event_id}/bookings` | Get bookings for specific event |
| `GET` | `/events/{event_id}/available-tickets` | Get available tickets for event |
| `GET` | `/events/{event_id}/revenue` | Calculate total revenue for event |

### Venues Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/venues` | Create a new venue |
| `GET` | `/venues` | Get all venues |
| `GET` | `/venues/{venue_id}/events` | Get events at specific venue |
| `GET` | `/venues/{venue_id}/occupancy` | Get venue occupancy statistics |

### Ticket Types Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ticket-types` | Create a new ticket type |
| `GET` | `/ticket-types` | Get all ticket types |
| `GET` | `/ticket-types/{type_id}/bookings` | Get bookings for specific ticket type |

### Bookings Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/bookings` | Create a new booking |
| `GET` | `/bookings` | Get all bookings with details |
| `PUT` | `/bookings/{booking_id}` | Update booking details |
| `DELETE` | `/bookings/{booking_id}` | Cancel a booking |
| `PATCH` | `/bookings/{booking_id}/status` | Update booking status |

### Advanced Queries
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/bookings/search` | Search bookings by filters |
| `GET` | `/booking-system/stats` | Get booking statistics |

## 🗄️ Database Schema

### Core Entities

#### Venue
- `id`: Primary key
- `name`: Unique venue name
- `location`: Venue address/location
- `capacity`: Maximum capacity
- `created_at`: Creation timestamp

#### Event
- `id`: Primary key
- `name`: Event name
- `description`: Event description
- `venue_id`: Foreign key to Venue
- `start_time`: Event start datetime
- `end_time`: Event end datetime
- `created_at`: Creation timestamp

#### TicketType
- `id`: Primary key
- `name`: Unique ticket type name
- `price`: Ticket price (DECIMAL)
- `created_at`: Creation timestamp

#### Booking
- `id`: Primary key
- `event_id`: Foreign key to Event
- `venue_id`: Foreign key to Venue
- `ticket_type_id`: Foreign key to TicketType
- `quantity`: Number of tickets
- `total_price`: Total booking cost
- `status`: Booking status (pending/confirmed/cancelled)
- `confirmation_code`: Unique confirmation code
- `created_at`: Creation timestamp

### Database Relationships
- **One-to-Many**: Event → Bookings, Venue → Events, TicketType → Bookings
- **Many-to-One**: Bookings → Event, Events → Venue, Bookings → TicketType
- **Cascade Operations**: Deleting events/venues/ticket types cascades to related bookings
- **Foreign Key Constraints**: Ensures data integrity

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database ORM**: SQLAlchemy 2.0
- **Database**: SQLite (development)
- **Data Validation**: Pydantic
- **API Documentation**: Automatic OpenAPI/Swagger
- **CORS**: Cross-Origin Resource Sharing enabled
- **Static Files**: Served via FastAPI StaticFiles

## 📦 Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
```

## 🎯 Key Features

### 🔐 Data Integrity
- Foreign key constraints prevent orphaned records
- Unique constraints on critical fields
- Cascade operations maintain referential integrity

### 💰 Revenue Tracking
- Automatic total price calculation
- Revenue reporting by event and venue
- Ticket type-based revenue analysis

### 📈 Capacity Management
- Venue capacity enforcement
- Real-time availability tracking
- Occupancy statistics

### 🔍 Advanced Search
- Filter bookings by event, venue, and ticket type
- Comprehensive booking statistics
- Revenue and occupancy analytics

### 🎨 User Interface
- Modern web interface for booking management
- Real-time data updates
- Responsive design

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📝 API Examples

### Create a Venue
```bash
curl -X POST "http://localhost:8000/venues" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Theater",
    "location": "123 Main St, City",
    "capacity": 500
  }'
```

### Create an Event
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rock Concert 2024",
    "description": "Amazing rock concert",
    "venue_id": 1,
    "start_time": "2024-06-15T19:00:00",
    "end_time": "2024-06-15T22:00:00"
  }'
```

### Create a Booking
```bash
curl -X POST "http://localhost:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "venue_id": 1,
    "ticket_type_id": 1,
    "quantity": 2
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using FastAPI and SQLAlchemy**