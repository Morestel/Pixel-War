<script setup>
import ChooseColor from './components/ChooseColor.vue';

</script>

<template>
  <svg id="pixel-select" width="3000" height="3000">
    <foreignObject :x="calc.x" :y="calc.y" :width="size_pixel" :height="size_pixel"><img src="./assets/pixel-select.png" alt=""></foreignObject>
  </svg>
  <canvas id="pixel-war" width="3000" height="3000" @click="clicCanvas($event)" style="position:absolute;"></canvas>
  <ChooseColor @select="colorSelected($event)" @valid="putPoint()"></ChooseColor>
  
  
</template>

<script>

    var pusher = new Pusher('de4f43d4d2ef0b884d48', {
      cluster: 'eu'
    });

    var channel = pusher.subscribe('my-channel');
   

export default {
  data: () => ({
    canvas : '',
    ctx : Object,
    coordinate_x: 0,
    coordiate_y: 0,
    size_pixel : 10,
    color: '#fff',
    calc: {x:0, y:0, color:'#fff'}  
  }),

  emits: ['select', 'valid'],

  mounted(){
    
    channel.bind('my-event', data => {this.updateNom(data)});
    channel.bind('draw-point', data => {this.drawPoint(data)});
    this.initCanvas()
    this.loadData()
  },

  watch:{
    coordinate_x: function(newX, oldX){ // Update of the calc
      console.log('Old : ' + oldX)
      console.log('New : ' + newX)
    }
  },

  methods:{

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
      // Now we update the calc
      this.updateCalc(this.coordinate_x, this.coordinate_y);

    },

    updateCalc: function(newX, newY){
      // this.ctx.globalAlpha = 0.5
      // this.ctx.fillStyle = this.calc.color;
      let x = newX - newX % this.size_pixel;
      let y = newY - newY % this.size_pixel;
      // this.ctx.fillRect(x, y, this.size_pixel, this.size_pixel);
      // this.ctx.globalAlpha = 1

      this.calc.x = x;
      this.calc.y = y;
    },

    putPoint: function(){ // Active when we validate the point, we draw it on the canvas
      let x = this.coordinate_x - this.coordinate_x % this.size_pixel
      let y = this.coordinate_y - this.coordinate_y % this.size_pixel
      let data = {x : x, y : y, color: this.color}

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
      this.ctx.fillRect(data.x, data.y, this.size_pixel, this.size_pixel)
      console.log('Drawing point at x: ' + data.x + ', y: '+ data.y)
    },

    colorSelected: function(event){
      this.color = event
    }
  }
}



</script>


<style>
@import './assets/base.css';

*{
  margin:0;
  padding:0;
}

html, body{
  min-width: 100%;
  min-height: 100%;
}

#pixel-select{
  position:absolute;
}

#pixel-select img{
  margin:0;
  top:0;
  padding: 0;
  position: absolute;
}

</style>
