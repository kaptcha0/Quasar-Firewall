const express = require('express')
const bodyParser = require('body-parser')
const app = express();

app.use(bodyParser.json())

app.use((req, res, next) => {
    console.log(`${req.method} REQUEST: '${req.url}'; BODY: ${JSON.stringify(req.body)}`)
    next()
})

app.get('/', (req, res) => {
    res.send("hello world")
});

app.get('/proxy', (req, res) => {
    res.send("proxy works");
});

app.post('/postable', (req, res) => {
    res.send(req.body)
})

const listener = app.listen(8080, () => {
    console.log("Started on ", listener.address())
})