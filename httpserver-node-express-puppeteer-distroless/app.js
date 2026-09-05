
require('dotenv').config();
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const RateLimit = require("express-rate-limit");

const { PROTECT_ROUTES, API_KEY } = process.env;

const indexRouter = require("./routes/index");
const app = express();

const limiter = RateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // max 100 requests per windowMs
});

app.use(limiter);
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

app.use((req, res, next) => {
    if (PROTECT_ROUTES) {
        const { api_key } = req.body;
        if (API_KEY === api_key) {
            next()
            return;
        }
        res.statusCode = 401;
        res.json({
            message: 'not_authorised_to_use_api'
        })
    }
    else {
      next();
    }

    return;
});

app.use("/", indexRouter);

module.exports = app;
