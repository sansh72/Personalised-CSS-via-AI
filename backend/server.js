const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const app = express();
const port = 5000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Set up the CSV writer for clicks
const csvWriter = createCsvWriter({
  path: 'clicks.csv',
  header: [
    {id: 'component', title: 'COMPONENT'},
    {id: 'clicks', title: 'CLICKS'},
    {id: 'timestamp', title: 'TIMESTAMP'},
    {id: 'datestamp', title: 'DATESTAMP'},
    {id: 'username', title: 'USERNAME'}
  ],
  append: true // If file exists, append to it; otherwise, create a new file
});

// Set up the CSV writer for login usernames
const usernameCsvWriter = createCsvWriter({
  path: 'clicks.csv',
  header: [
    {id: 'component', title: 'COMPONENT'},
    {id: 'clicks', title: 'CLICKS'},
    {id: 'timestamp', title: 'TIMESTAMP'},
    {id: 'datestamp', title: 'DATESTAMP'},
    {id: 'username', title: 'USERNAME'}
  ],
  append: true
});

// Route to handle saving click data
app.post('/api/save-clicks', (req, res) => {
  const { component, clicks, timestamp, datestamp, username } = req.body;

  // Convert the username to uppercase
  const uppercaseUsername = username.toUpperCase();

  const clickData = [{
    component,
    clicks,
    timestamp,
    datestamp,
    username: uppercaseUsername
  }];

  csvWriter.writeRecords(clickData)
    .then(() => {
      console.log('Click data saved to CSV file');
      res.send('Data saved');
    })
    .catch(err => {
      console.error('Error saving click data to CSV:', err);
      res.status(500).send('Error saving click data');
    });
});

// Route to handle saving login username
app.post('/api/register-username', (req, res) => {
  const { username } = req.body;

  // Convert the username to uppercase
  const uppercaseUsername = username.toUpperCase();

  const loginData = [{
    username: uppercaseUsername,
    loginTime: new Date().toISOString()
  }];

  usernameCsvWriter.writeRecords(loginData)
    .then(() => {
      console.log(`Username ${uppercaseUsername} saved to CSV file`);
      res.send(`Username ${uppercaseUsername} registered`);
    })
    .catch(err => {
      console.error('Error saving username to CSV:', err);
      res.status(500).send('Error registering username');
    });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
