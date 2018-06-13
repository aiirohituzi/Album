<template>
<div class="container-main">
    <div class="wrapper-sign">
        <h2>관리자 계정 로그인</h2>
        <div class="input-group">
            <input type="text" placeholder="ID"><br>
            <input type="text" placeholder="PW"><br>
        </div>
        <button class="sign-in">Sign in</button>
    </div>
</div>
</template>

<script>
</script>

<style>
.container-main {
    margin-top: 20px;
    margin-left: 10px;
}
.wrapper-sign {
    width: 300px;
    height: 350px;
    text-align: center;
    margin-top: 20vh;
    margin-left: auto;
    margin-right: auto;
    background-color: #faaf40;
    -moz-box-shadow: 2px 2px 4px #333;
    -webkit-box-shadow: 2px 2px 4px #333;
    box-shadow: 2px 2px 4px #333;
    border: 1px solid #faaf40;
    border-radius: 5px;
}
.wrapper-sign h2{
    margin-top: 50px;
    margin-bottom: 50px;
}
.wrapper-sign .input-group {
    /* margin-top: 30vh; */
}
.wrapper-sign .input-group input{
    margin: 10px;
    width: 200px;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 3px;
}
.wrapper-sign .sign-in{
    margin-top: 10px;
    margin-left: auto;
    margin-right: auto;
    width: 200px;
    background-color: #1175cc;
    border-radius: 3px;
    padding-top: 5px;
    padding-bottom: 5px;
}
.wrapper-sign .sign-in:hover{
    background-color: #1165cc;
}
</style>