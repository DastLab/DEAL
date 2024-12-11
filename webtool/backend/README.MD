# DEAL Backend - NodeJS required

Installation instruction (run command from current folder). We assume that NodeJS and MongoDB are correctly installed on the system and that a **deal/json_results** collection has already been created.

The following command installs the project dependencies.
```
npm install
```

To run the backend server, use the following command

```
node server.js -p 5000 -m mongodb://localhost:27017/deal
```

The meaning of the parameters is listed below:

1. **-p** specifies the server's listening port
2. **-m** specifies the mongo database connection url

