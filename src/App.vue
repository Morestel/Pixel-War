<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
</script>

<template>
  Slt
  <input v-model="nom" />
  <button @click="envoyerMsg()">Envoyer</button>
  {{ nom }}
  <br>
  <canvas id="pixel-war" width="500" height="500" @click="clicCanvas($event)"></canvas>
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
  }),

  mounted(){
    
    channel.bind('my-event', data => {this.updateNom(data)});
    this.initCanvas()
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

    updateNom: function(data){
      this.nom = data.message
    },

    initCanvas: function(){
      this.canvas = document.getElementById('pixel-war');
      console.log(this.canvas)
      this.ctx = this.canvas.getContext('2d')
      console.log(this.ctx)
    },

    clicCanvas: function(event){ // When a user clic we retrieve the coordinates of the click
      this.coordinate_x = event.offsetX;
      this.coordinate_y = event.offsetY;
      console.log('x: ' + this.coordinate_x + ', y: '+ this.coordinate_y)
      let data = {x : this.coordinate_x, y : this.coordinate_y, color: '#ff0000'}

      this.drawPoint(data)
    },

    drawPoint: function(data){ // Function use to draw a point after a click
    console.log(data.x + ' ' + data.y)
      this.ctx.fillStyle = data.color
      let x = data.x%10
      console.log(x)
      this.ctx.fillRect(data.x, data.y, 10, 10)
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
