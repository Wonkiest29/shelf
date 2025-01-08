const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const app = express();
const port = 3000;

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware to parse cookies
app.use(cookieParser());

// Serve static files from the "pub" directory
app.use(express.static(path.join(__dirname, 'pub')));
app.use('/node_modules', express.static(path.join(__dirname, './node_modules')));

app.get('/', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('index', { title: 'Items', token });
});

app.get('/login', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('signin', { title: 'Login', token });
});

app.get('/register', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('register', { title: 'Register', token });
});

app.get('/users', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('users', { title: 'Users', token });
});

app.get('/settings', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('settings', { title: 'Settings', token });
});

app.get('/items', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    res.render('items', { title: 'Items', token });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});