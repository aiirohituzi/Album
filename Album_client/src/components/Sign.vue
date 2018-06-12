<template>
<div class="container-main">
    <div class="wrapper-sign">
        <h2>관리자 계정 로그인</h2>
        <div class="input-group">
            <input type="text" placeholder="ID"><br>
            <input type="text" placeholder="PW"><br>
        </div>
        <div class="sign-in">Sign in</div>
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
    border: 1px solid #111;
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