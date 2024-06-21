import styled from 'styled-components'
export const Hoome = styled.div`
    height: 700px;
    // background-image: url("images/Home/home-bg.jpg");
     background-image: url("images/Home/OIP5.jpg");
    background-size: cover;
    width:100%;
    background-position:center ;
    text-align: center;
    position: relative;
    background-attachment: fixed;
    padding-bottom: 20%;
    // opacity:0.93;
    `


export const Container = styled.div`
    width: 50%;
    position: absolute;
    top: 35%;
    left:55%;
    transform:translate(-50%,-50%)
`


export const Hometitle = styled.h2`
background: linear-gradient(45deg, #ff0000, #00ff4e);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
    // margin-top: 50%;
    margin-right:-80%;
    font-weight: bold;
    font-size:60px;
    // color: #eb5424;
    // color: #707070;
    margin-top:1%;
    // margin-bottom:7%;
    font-style: italic;

`


export const Homeinfo = styled.h4`
    margin-bottom: 20px;
    font-size:35px;
    color:#eb5424
    `



export const Homedesc = styled.p`
    font-size: 20px;
    line-height: 1.5;
    color: #888;
    margin-bottom: 20px;
`



export const Span = styled.span`
    color: #000
`

export const Homebtn = styled.button`
    padding: 15px ;
    width: 150px;
    background-color:#eb5424;
    color: white;
    border:none;
    font-size: 18px;
    font-weight: bold;

    &:hover
        {
            color:#eb5424;
            background-color: white;
        }
`