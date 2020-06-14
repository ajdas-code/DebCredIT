'use strict';
const Confidence = require('confidence');
const Dotenv = require('dotenv');


Dotenv.config({ silent: true });

const criteria = {
    env: process.env.NODE_ENV
};


const config = {
    $meta: 'This file configures the plot device.',
    projectName: 'Aqua',
    port: {
        web: {
            $filter: 'env',
            test: 9000,
            production: process.env.PORT,
            $default: 8000
        }
    },
    baseUrl: {
        $filter: 'env',
        $meta: 'values should not end in "/"',
        production: 'https://debcredit.gcp.com:8000',
        $default: 'http://127.0.0.1:8000'
    },
    authAttempts: {
        forIp: 50,
        forIpAndUser: 7
    },
    cookieSecret: {
        $filter: 'env',
        production: process.env.COOKIE_SECRET,
        $default: '!k3yb04rdK4tz~4qu4~k3yb04rdd0gz!'
    },
    hapiMongoModels: {
        mongodb: {
            uri: {
                $filter: 'env',
                production: process.env.MONGODB_URI,
                test: 'mongodb://testuser:testuser@kitchensink-shard-00-00-lzcqm.mongodb.net:27017,kitchensink-shard-00-01-lzcqm.mongodb.net:27017,kitchensink-shard-00-02-lzcqm.mongodb.net:27017/test?ssl=true&replicaSet=kitchensink-shard-0&authSource=admin&retryWrites=true&w=majority',
                $default: 'mongodb://testuser:testuser@kitchensink-shard-00-00-lzcqm.mongodb.net:27017,kitchensink-shard-00-01-lzcqm.mongodb.net:27017,kitchensink-shard-00-02-lzcqm.mongodb.net:27017/test?ssl=true&replicaSet=kitchensink-shard-0&authSource=admin&retryWrites=true&w=majority'
            }
        },
        autoIndex: true
    },
    nodemailer: {
        host: 'smtp.zohomail.com',
        port: 465,
        secure: true,
        auth: {
            user: 'dajitesh@zohomail.com',
            pass: process.env.SMTP_PASSWORD
        }
    },
    system: {
        fromAddress: {
            name: 'DebCredIT',
            address: 'dajitsh@zohomail.com'
        },
        toAddress: {
            name: 'DebCredIT',
            address: 'dajitesh@zohomail.com'
        }
    }
};


const store = new Confidence.Store(config);


exports.get = function (key) {

    return store.get(key, criteria);
};


exports.meta = function (key) {

    return store.meta(key, criteria);
};
