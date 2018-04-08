<template>
<ul id="navigation">
   <li><a>1</a></li>
   <li><a>2</a></li>
   <li><a>3</a></li>
   <li><a>4</a></li>
   <li><a>5</a></li>
</ul>
</template>

<script>
</script>

<style>
ul#navigation {
    position: fixed;
    margin: 0px;
    padding: 0px;
    top: 0px;
    left: 0px;
    width: 300px;
    height: 100%;
    list-style: none;
    z-index:9999;
}
ul#navigation li {
    width: 100%;
    height: 20%;
}
ul#navigation li a {
    display: block;
    margin-left: 0px;
    width: 100%;
    height: 99%;
    background-color:#CFCFCF;
    background-repeat:no-repeat;
    background-position:center center;
    border:1px solid #AFAFAF;
    -moz-box-shadow: 0px 2px 3px #333;
    -webkit-box-shadow: 0px 2px 3px #333;
    box-shadow: 0px 2px 3px #333;
}        
</style>