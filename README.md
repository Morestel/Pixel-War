# Pixel-War

Website of a Pixel War game between lots of users. Inspired by the [r/Place](https://www.reddit.com/r/place/) of Reddit 

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development
Launch the website
```sh
npm run dev
```

Launch the server
```sh
uvicorn server:app --reload
```

### Compile and Minify for Production

```sh
npm run build
```

### TODO
- Connect a database and store the different point, once a user connects he receive all the point
- Display the coordinate of the canvas
- Display a square where the user is
- Make possible the shift with the arrow keys
- Change the range of the colors