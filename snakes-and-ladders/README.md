# Snakes and Ladders Game

A modern, full-stack Snakes and Ladders game with a React frontend and Flask backend API.

## Features

### Frontend (React)
- **Interactive dice rolling** with animation
- **Visual snakes and ladders** that extend to their destinations
- **Colorful board** with alternating yellow and green cells
- **Responsive design** for desktop and mobile
- **Game status updates** with emoji feedback
- **Winner celebration** with modal popup
- **Reset functionality** to start new games

### Backend (Flask API)
- **User authentication** with JWT tokens
- **User registration and login**
- **Game state management**
- **Multiplayer support**
- **Database persistence** with SQLAlchemy
- **RESTful API endpoints**

## Game Rules

- Players take turns rolling the dice
- Move your token according to the dice roll
- **Ladders** help you climb up faster
- **Snakes** slide you down
- Rolling a 6 gives you an extra turn
- First player to reach cell 100 wins!

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

#### Frontend Setup
1. Clone the repository:
```bash
git clone https://github.com/blankops-000/phase-2-snakes-n-laders.git
cd phase-2-snakes-n-laders/snakes-and-ladders
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

#### Backend Setup
1. Navigate to the Flask project directory:
```bash
cd ../flask_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install flask flask-cors flask-migrate flask-jwt-extended flask-sqlalchemy werkzeug
```

4. Start the Flask server:
```bash
python app.py
```

5. The API will be available at `http://localhost:5001`

## Game Elements

### Snakes Positions
- 16 → 6, 47 → 26, 49 → 11, 56 → 53, 62 → 19
- 87 → 24, 93 → 73, 95 → 75, 98 → 78

### Ladders Positions
- 1 → 38, 4 → 14, 9 → 21, 28 → 84, 36 → 44
- 51 → 67, 71 → 91, 80 → 100

## Technologies Used

### Frontend
- **React** - Frontend framework
- **Vite** - Build tool and dev server
- **CSS** - Styling and animations

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Migrate** - Database migrations

## Responsive Design

The game is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## How to Play

1. Click "Roll Dice" to start your turn
2. Your token moves automatically based on the dice roll
3. Land on a ladder bottom to climb up
4. Land on a snake head to slide down
5. First to reach cell 100 wins!

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Project Structure

```
snakes_and_ladders_3.0/
├── snakes-and-ladders/          # React Frontend
│   ├── src/
│   │   ├── Component/
│   │   │   ├── GameBoard.jsx    # Main game board
│   │   │   ├── DiceRoller.jsx   # Dice rolling component
│   │   │   ├── GameStatus.jsx   # Game status display
│   │   │   └── *.css           # Component styles
│   │   ├── assets/
│   │   │   ├── snake-straight.svg
│   │   │   └── ladder-transparent.svg
│   │   └── App.jsx             # Main app component
│   └── package.json
└── flask_project/              # Flask Backend
    ├── app.py                  # Main Flask application
    ├── models.py               # Database models
    ├── config.py               # Configuration settings
    └── requirements.txt        # Python dependencies
```

## API Endpoints

- `GET /` - API status and available endpoints
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /my-game` - Get user's active game
- `POST /start-game` - Start a new game
- `POST /roll-dice` - Roll dice and move player
- `GET /game-state/<game_id>` - Get current game state

## Customization

You can easily customize:
- Snake and ladder positions in `App.jsx`
- Board colors in `GameBoard.css`
- Player token colors
- Game messages and emojis

## Contributors

- **Ignatius** - Backend Development
- **Tiara** - Frontend Development
- **Michelle** - UI/UX Design
- **Erick** - Full-stack Development

---

Enjoy playing Snakes and Ladders! 