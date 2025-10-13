import express from "express";

const app = express();
const port = 3000;

app.get("/", (req, res) => {
    // redirect to /main
})

app.get("/main", (req, res) => {
    // render main_page.html
})

/* 
app.post("/main", (req, res) => {
    // insert order to db (to delete)
})
*/

app.get("/contacts", (req, res) => {
    // render contacts.html
})

app.get("/order", (req, res) => {
    // render order.html
})

app.get("/comments", (req, res) => {
    // render comments.html
})

app.post("/comments", (req, res) => {
    // publish coment and stay on the same page
})

app.listen(port, () => {
    console.log("Server running on port 3000.");
})