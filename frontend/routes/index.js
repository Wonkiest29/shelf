const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.render('index', { title: 'Items' });
});

router.get('/login', (req, res) => {
    res.render('signin', { title: 'Login' });
});

router.get('/register', (req, res) => {
    res.render('signup', { title: 'Register' });
});

router.get('/users', (req, res) => {
    res.render('users', { title: 'Users' });
});

router.get('/settings', (req, res) => {
    res.render('settings', { title: 'Settings' });
});

router.get('/items', (req, res) => {
    res.render('items', { title: 'Items' });
});

module.exports = router;