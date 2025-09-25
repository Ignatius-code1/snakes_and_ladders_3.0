-- Create games table
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    current_turn INTEGER DEFAULT 0,
    winner_id UUID REFERENCES auth.users(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create game_players table
CREATE TABLE game_players (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id),
    position INTEGER DEFAULT 0,
    player_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE games ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_players ENABLE ROW LEVEL SECURITY;

-- Create policies for games table
CREATE POLICY "Users can view games they participate in" ON games
    FOR SELECT USING (
        id IN (
            SELECT game_id FROM game_players 
            WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create games" ON games
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their games" ON games
    FOR UPDATE USING (
        id IN (
            SELECT game_id FROM game_players 
            WHERE user_id = auth.uid()
        )
    );

-- Create policies for game_players table
CREATE POLICY "Users can view their game participations" ON game_players
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create their game participations" ON game_players
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their game participations" ON game_players
    FOR UPDATE USING (user_id = auth.uid());