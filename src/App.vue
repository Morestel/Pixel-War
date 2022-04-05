<script setup>
import ChooseColor from './components/ChooseColor.vue';

</script>

<template>
  Slt
  <input v-model="nom" />
  <button @click="envoyerMsg()">Envoyer</button>
  {{ nom }}
  <br>
  <canvas id="pixel-war" width="500" height="500" @click="clicCanvas($event)"></canvas>
  <ChooseColor @select="colorSelected($event)" @valid="putPoint()"></ChooseColor>
</template>

<script>

    var pusher = new Pusher('de4f43d4d2ef0b884d48', {
      cluster: 'eu'
    });

    var channel = pusher.subscribe('my-channel');
   

export default {
  data: () => ({
    ds : null,
    nom :'',
    canvas : '',
    ctx : Object,
    coordinate_x: 0,
    coordiate_y: 0,
    size_pixel : 10,
    color: '#fff',
  }),

  emits: ['select', 'valid'],

  mounted(){
    
    channel.bind('my-event', data => {this.updateNom(data)});
    channel.bind('draw-point', data => {this.drawPoint(data)});
    this.initCanvas()
    this.loadData()
  },

  methods:{
    async envoyerMsg(){
    let url = 'http://localhost:8000/api/test'
    let data = {
      nom : this.nom
    }
    let res = await fetch(url, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(data),
              });
    },

    async loadData(){
      let url = 'http://localhost:8000/api/get_all'
      let res = await fetch(url)
      let data = await res.json()
      console.log(data["pixels"])
      data.pixels.forEach(element => {
        let pixel = {x : element[0], y : element[1], color : element[2]}
        this.drawPoint(pixel)
      });
    },

    updateNom: function(data){
      this.nom = data.message
    },

    initCanvas: function(){
      this.canvas = document.getElementById('pixel-war');
      this.ctx = this.canvas.getContext('2d')
    },

    clicCanvas: function(event){ // When a user clic we retrieve the coordinates of the click
      this.coordinate_x = event.offsetX;
      this.coordinate_y = event.offsetY;
      console.log('x: ' + this.coordinate_x + ', y: '+ this.coordinate_y)
      
    },

    putPoint: function(){ // Active when we validate the point, we draw it on the canvas
      let data = {x : this.coordinate_x, y : this.coordinate_y, color: this.color}

      this.drawPoint(data) // We draw the point
      this.sendPoint(data) // We send the point to the others
    },

    async sendPoint(data){
      let url = 'http://localhost:8000/api/draw'
      let res = await fetch(url, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(data),
              });
    },

    drawPoint: function(data){ // Function use to draw a point after a click
      this.ctx.fillStyle = data.color
      let x = data.x - data.x%this.size_pixel
      let y = data.y - data.y%this.size_pixel
      this.ctx.fillRect(x, y, this.size_pixel, this.size_pixel)
      console.log('Drawing point at x: ' + x + ', y: '+ y)
    },

    colorSelected: function(event){
      this.color = event
      console.log(this.color)
    }
  }
}



</script>


<style>
@import './assets/base.css';

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

@media (min-width: 1024px) {
  body {
    display: flex;
    place-items: center;
  }

  #app {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 2rem;
  }

  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>
