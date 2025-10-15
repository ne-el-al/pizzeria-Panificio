import express from "express";
// import morgan from "morgan"
import { database } from "./db_connection.js";

const app = express();

database.connect(function (err) {
    if (err) return err;
    console.log("Connected!");
});

app.use(express.static('public'));
// app.use(express.static('images'));

// app.use(morgan("tiny"));

app.set("view engine", "ejs")
const port = 3000;

// installing connection to database



app.get("/", (req, res) => {
    res.render("index.ejs",
        {
            page: "main.ejs"
        }
    );
})

app.get("/order", (req, res) => {
    res.render("index.ejs",
        {
            page: "order.ejs"
        }
    )
})

app.get("/menu", (req, res) => {
    try {
        database.execute('SELECT * FROM food', function (error, results, fields) {
            if (error) throw error;
            // console.log(results);
            res.render("index.ejs", {
                result: results,
                page: "menu.ejs"
            }
            )
        });

    }
    catch (error) {
        console.log(error);
    }
})

app.get("/menu/:menuId", (req, res) => {
    const menuId = req.params.menuId;
    console.log("menuId:", menuId);

    database.query("SELECT * FROM food WHERE id = ?", [menuId], (err, result) => {
        if (err) {
            console.error(err);
            return res.status(500).send("Database error");
        }

        console.log(result.length);

        if (result.length > 1 || result.length <= 0) {
            res.redirect("/");
        }
        else {
            res.render("index.ejs", {
                page: "menu_card.ejs",
                food: result[0],
            });
        }


    });
});

app.get("/discount", (req, res) => {
    res.render("index.ejs",
        {
            page: "discount.ejs"
        }
    )
})

app.get("/contacts", (req, res) => {
    res.render("index.ejs",
        {
            page: "contacts.ejs"
        }
    )
})

app.get("/comments", (req, res) => {
    res.render("index.ejs",
        {
            page: "comments.ejs"
        }
    )
})

app.listen(port, () => {
    console.log("Server running on port 3000.");
})