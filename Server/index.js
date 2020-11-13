const express = require('express')
const bodyParser = require('body-parser')
const app = express();


function process(req) {
}

app.use(bodyParser.json())

app.use((req, res, next) => {
    console.log(`REQUEST: '${req.url}'`)
    process(req)
    next()
})

app.get('/', (req, res) => {
    res.send("hello world")
});

app.get('/proxy', (req, res) => {
    res.send("proxy works");
});

app.post('/postable', (req, res) => {
    console.log(req.body)
    res.send(req.body)
})

const listener = app.listen(8080, () => {
    console.log("Started on ", listener.address())
})