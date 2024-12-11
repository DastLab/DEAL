# DEAL Frontend

Installation instruction (run command from current folder).

The following command installs the project dependencies.
```
npm install
```

To run the frontend, use the following command

```
npm start
```

It is possible to change the backend connection url by modifying the variable REACT_APP_BACKEND variable in the .env file

```
REACT_APP_BACKEND=http://SERVER:PORT
```

The API KEYs for the communication with ChatGPT, Llama, and Gemma can be set by the properties
```
REACT_APP_API_KEY_CHATGPT=secret
REACT_APP_API_KEY_LLAMA=secret
REACT_APP_API_KEY_GEMMA=secret
```