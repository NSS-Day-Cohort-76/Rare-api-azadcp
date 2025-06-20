DROP TABLE IF EXISTS DemotionQueue;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS PostReactions;
DROP TABLE IF EXISTS PostTags;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    bio TEXT,
    username TEXT,
    password TEXT,
    profile_image_url TEXT,
    created_on DATE,
    active BOOLEAN,
    isAdmin BOOLEAN DEFAULT 0,
    isAuthor BOOLEAN DEFAULT 0
);

CREATE TABLE DemotionQueue (
    action TEXT,
    admin_id INTEGER,
    approver_one_id INTEGER,
    PRIMARY KEY (action, admin_id, approver_one_id),
    FOREIGN KEY(admin_id) REFERENCES Users(id),
    FOREIGN KEY(approver_one_id) REFERENCES Users(id)
);

CREATE TABLE Subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follower_id INTEGER,
    author_id INTEGER,
    created_on DATE,
    FOREIGN KEY(follower_id) REFERENCES Users(id),
    FOREIGN KEY(author_id) REFERENCES Users(id)
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category_id INTEGER,
    title TEXT,
    publication_date DATE,
    image_url TEXT,
    content TEXT,
    approved BOOLEAN,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(category_id) REFERENCES Categories(id)
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    author_id INTEGER,
    content TEXT,
    FOREIGN KEY(post_id) REFERENCES Posts(id),
    FOREIGN KEY(author_id) REFERENCES Users(id)
);

CREATE TABLE Reactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT,
    image_url TEXT
);

CREATE TABLE PostReactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reaction_id INTEGER,
    post_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(reaction_id) REFERENCES Reactions(id),
    FOREIGN KEY(post_id) REFERENCES Posts(id)
);

CREATE TABLE Tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT
);

CREATE TABLE PostTags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(post_id) REFERENCES Posts(id),
    FOREIGN KEY(tag_id) REFERENCES Tags(id)
);

-- Seed data
INSERT INTO Users (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active, isAdmin, isAuthor) VALUES
('Jamie', 'Smith', 'jamie@example.com', 'Photographer and foodie.', 'jamies', 'password123', '', '2025-06-01', 1, 1, 1),
('Riley', 'Jones', 'riley@example.com', 'Lover of coffee and cats.', 'rjones', 'password123', 'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg', '2025-06-02', 1, 0, 1),
('Taylor', 'Lee', 'taylor@example.com', 'News junkie and podcast addict.', 'tlee', 'password123', '', '2025-06-03', 1, 0, 1),
('Jordan', 'Kim', 'jordan@example.com', 'DIY enthusiast. Posts every Sunday.', 'jkim', 'password123', '', '2025-06-04', 1, 0, 1),
('Morgan', 'Ray', 'morgan@example.com', 'Weekend brunch warrior.', 'mray', 'password123', '', '2025-06-05', 1, 0, 1);

INSERT INTO Categories (label) VALUES
('News'), ('Politics'), ('Sports'), ('Local'), ('Events'), ('Classifieds');

INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES
(1, 3, 'Game Recap: Titans vs Jaguars', '2025-06-10', '', 'The Titans held on for a dramatic win...', 1),
(2, 4, 'Hidden Gems: Nashville Coffee Spots', '2025-06-11', '', 'Check out these lesser-known cafés...', 1),
(3, 1, 'Local Elections: What You Need to Know', '2025-06-12', '', 'Early voting begins this week...', 1),
(4, 5, 'This Weekend: Free Events Around Town', '2025-06-13', '', 'From farmers markets to outdoor concerts...', 1),
(5, 6, 'Classifieds: Roommate Wanted in East Nash', '2025-06-14', '', 'Looking for a roommate, $950/mo...', 1);

INSERT INTO Comments (post_id, author_id, content) VALUES
(1, 2, 'Great recap! I missed the game.'),
(2, 3, 'Brb, heading to that new coffee shop now ☕️'),
(3, 4, 'Thanks for the election rundown, super helpful.'),
(4, 1, 'See y’all at the farmers market!'),
(5, 2, 'Is this still available?');

INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES
(2, 1, '2025-06-06'),
(3, 1, '2025-06-06'),
(4, 2, '2025-06-07'),
(5, 3, '2025-06-08'),
(1, 4, '2025-06-09');

INSERT INTO Tags (label) VALUES
('JavaScript'), ('Nashville'), ('Food'), ('Brunch'), ('Music'), ('Outdoors');

INSERT INTO Reactions (label, image_url) VALUES
('happy', 'https://pngtree.com/so/happy');
