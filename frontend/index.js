const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the "pub" directory
app.use(express.static(path.join(__dirname, 'pub')));

// Serve static files from the "node_modules" directory
app.use('/node_modules', express.static(path.join(__dirname, './node_modules')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'pub', 'index.html'));
});

app.listen(port, () => {
  console.log(`Frontend server listening at http://localhost:${port}`);
});