import express from "express"

import crypto from "crypto"     //install

import cors from "cors"
import mongoose from "mongoose"
// import {userSchema} from "./models/User.js"
import dotenv, { config } from 'dotenv'
import path, { resolve } from 'path'
import {fileURLToPath} from 'url';
import { userRoutes } from "./routes/userRoutes.js"
import {GridFsStorage} from "multer-gridfs-storage"  //install the dependencies. try with regular method, if that doesnt work try (npm i multer-gridfs-storage  --force)
import multer from "multer"          //install the dependencies. try with regular method, if that doesnt work try (npm i multer --force)


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, '.env') });

const DB="mongodb+srv://sawara:sawara@cluster0.cwpdwv8.mongodb.net/medical?retryWrites=true&w=majority"        //change this to your atlas login URL

const app = express()
app.use(express.json())
app.use(express.urlencoded())
app.use(cors())

// mongoose.connect(process.env.DB_URI,  { 
//     useNewUrlParser: true,
//     useUnifiedTopology: true
// }, () => {
//     console.log("DB connected")
// })

    mongoose.connect(DB, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    
}).then(()=>{
    console.log("connected successfully !");
}).catch((err)=>{

    console.log(err);
})

process.on('unhandledRejection', error =>{
    console.log('unhandledRejection', error.message);
});

// creating a bucket for storage

var bucket;
mongoose.connection.on('storing', ()=> {
    // var db_con = mongoose.connections[0].db_con;
    var db = mongoose.connections[0].db;
    bucket = new mongoose.mongo.GridFSBucket(db, {
    bucketName: "med_data"
      });
      console.log(bucket);
    });

    //to parse json content
    app.use(express.json());
    
    //to parse body from url
    app.use(express.urlencoded({
    extended: false
    }));

const storage = new GridFsStorage ({
    url: DB,
    file: (req,file) => {
        return new Promise ((resolve,reject) => {
            //encrypting file name  (used to generate a random id for filename. this will avoid conflict of same name)
            crypto.randomBytes(16, (err , buf) => {
                if (err){
                    return reject (err);
                }

                const filename = buf.toString ('hex') + path.extname (file.originalname);
                const fileInfo = {
                    filename: filename,
                    bucketName: 'med_id'
                };
                resolve (fileInfo);
            });
        });
    }
});

const upload = multer ({storage});

//used for retrieving file. there is some error over here, but im not sure
app.get("/fileinfo/:filename", (req, res) => {
    const file = bucket
      .find({
        filename: req.params.filename
      })
      .toArray((err, files) => {
        if (!files || files.length === 0) {
          return res.status(404)
            .json({
              err: "no files exist"
            });
        }
        bucket.openDownloadStreamByName(req.params.filename)
          .pipe(res);
      });
  });

  //file upload url. working properly 
app.post("/upload", upload.any('file'), (req,res) => {
    res.status(200).send("file uploaded");
});


app.listen(9002, ()=>{
    console.log("started at 9002 !")
});

app.use("/",userRoutes)



 
