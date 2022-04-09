<template>

    <div id="box" class="hidden">
        <ul>
            <li v-for="color in colors" :key="color"><div class="color-box" v-bind:style="{background: color}" @click="chooseColor(color)"></div></li>
        </ul>
        <div class="choice">
            <button @click="hide()">Annuler</button>
            <button @click="$emit('valid')">Valider</button>
        </div>
    </div>


</template>

<script>

export default{
    data: () => ({
        colors: {
            red: '#ff0000',
            blue: '#0000ff',
            green: '#00ff00',
            yellow: '#ffff00',
            purple: '#ff00ff',
            orange: '#ffa500',
            black: '#000000',
            white: '#ffffff',
            gray: '#808080',
            brown: '#8b4513',
            pink: '#ffc0cb',
            cyan: '#00ffff',
            magenta: '#ff00ff',
            lime: '#00ff00',
            silver: '#c0c0c0',
            maroon: '#800000',
            navy: '#000080',
            olive: '#808000',
            teal: '#008080',
            aqua: '#00ffff',
            fuchsia: '#ff00ff',
        }
    }),

    methods:{
        chooseColor: function(color){
            this.$emit('select', color)
        },

        hide: function(){
            // Hide the box
            let box = document.getElementById('box')
            box.classList.add('hidden')
            
        }
    }
}

</script>

<style scoped>

#box{
    width:150px;
    height: 85%;
    border: 1px solid red;
    position: fixed;
    right: 5px;
    top: 5px;
    border-radius: 5px;
    background: rgb(130, 130, 130);
    overflow-y:scroll;
    scrollbar-width: none;
    -ms-overflow-style: none;
    
}
/* Hide scrollbar for Chrome, Safari and Opera */
#box::-webkit-scrollbar {
  display: none;
}
#box ul{
    position: relative;
    list-style: none;
    text-align: center;
    margin-top:5px;
}

#box .choice{
    display: relative;
    margin: auto 0 auto 0;
}

.color-box {
    width: 60px;
    height: 30px;
    display: inline-block;
    margin: 0 5px;
    border: 1px solid #000;
    cursor: pointer;
}

.hidden{
    visibility: hidden;
}

</style>