import mysql from "mysql2"

export let database = mysql.createConnection({
    host: "",
    user: "",
    password: "",
    database: ""
})
