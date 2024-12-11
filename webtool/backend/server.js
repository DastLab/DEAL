const express = require('express');
const multer = require('multer');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const date = require('date-and-time')

const app = express();

const { Command } = require('commander');
const program = new Command();

program
    .name('DEAL backend');
program
    .requiredOption('-p, --listen_port [int]')
    .requiredOption('-m, --mongo_connection [string]')


program.parse();

const options = program.opts();

const port = options.listen_port
mongoose.connect(options.mongo_connection)
    .then(() => console.log('MongoDB connected'))
    .catch(err => {
        console.error('Error connecting to MongoDB:', err);
        process.exit(1);
    });

const jsonSchema = new mongoose.Schema({
        fileName: String,
        data: Object},
    {timestamps: true }
);

const JSONResults = mongoose.model('json_results', jsonSchema);

const upload = multer({ dest: 'uploads/' });

app.use(function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
});




app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        const filePath = req.file.path;
        const fileName = req.file.originalname;
        const rawData = fs.readFileSync(filePath);
        const jsonData = JSON.parse(rawData);

        const newJSON = new JSONResults({ fileName, data: jsonData });
        await newJSON.save();

        fs.unlinkSync(filePath);
        console.log(`File ${fileName} removed from multer's temporary folder`);

        res.send('JSON file uploaded and saved to MongoDB!');
    } catch (error) {
        console.error('Error uploading the file:', error);
        res.status(500).send('Error uploading JSON file');
    }
});

app.get('/files', async (req, res) => {
    try {
        const files = await JSONResults.find({}, '_id fileName createdAt').lean();
        res.json(files.map(file => ({
            ...file,
            createdAt: date.format(new Date(file.createdAt),"YYYY-MM-DD HH:mm:ss"),
            timestamp: new Date(file.createdAt).getTime()
        })));
    } catch (error) {
        console.error('Error retrieving file names:', error);
        res.status(500).json({ error: 'Error retrieving file names' });
    }
});

app.get('/files/:id', async (req, res) => {
    try {
        const file = await JSONResults.findById(req.params.id);
        if (!file) {
            return res.status(404).json({ error: 'File not found' });
        }
        res.json(file.data);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error retrieving file content' });
    }
});


app.delete('/files/:id', async (req, res) => {
    try {
        const fileId = req.params.id;
        const deletedFile = await JSONResults.findByIdAndDelete(fileId);
        if (!deletedFile) {
            return res.status(404).json({ error: 'File not found' });
        }
        res.json({ message: 'File deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error deleting the file' });
    }
});


app.use(express.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.put('/files/:id', async (req, res) => {
    try {
        const fileId = req.params.id;
        const { fileName } = req.body;

        const updatedFile = await JSONResults.findByIdAndUpdate(fileId, { fileName }, { new: true });

        if (!updatedFile) {
            return res.status(404).json({ error: 'File not found' });
        }

        res.json({ message: 'File name updated successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error updating file name' });
    }
});


app.listen(port, () => console.log(`Server running on port ${port}`));
