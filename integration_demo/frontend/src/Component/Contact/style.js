import styled from "styled-components";

export const Contactt = styled.div
`
    // margin-right:130px;
    // padding:50px 0px;
    text-align:center;
    background-image: url("/images/Home/OIP5.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position:center ;
    height: 2000px;
    padding-top: 20px;
    padding-bottom: 20%;

`

export const Container = styled.div
`
max-width: 600px;
margin-top: 5% ;
margin-left:28%;
padding: 20px;
/* background-color: rgba(59, 58, 58, 0.5); */
/* background-color: rgb(249, 249, 249); */
background-color:rgba(255,255,255,0.9);
border-radius: 8px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
color: #000;
`
export const Contacttitle = styled.h2
`
    color:#404040;
    font-size:40px;
    margin-bottom:30px;
`

export const Form = styled.form
`
    width:70%;
    margin:auto;

`
export const Input = styled.input
`
    width:100%
    box-sizing:border-box;
    outline:0;
    padding :5px;
    margin-bottom:10px;
`
export const Forminput = styled.div
`
    overflow:hidden;
`
export const Span = styled.span
`
    font-weight:normal; 
`
export const InputText = styled(Input)
`
    margin-right:2%;
    float:left;
    width:49%;
`
export const InputEmail = styled(Input)
`
    float:left;
    width:49%;
`
export const InputExp = styled(Input)
`
float:left;
    width:100%;
`
export const InputSubmit = styled(Input)
`
    width:60%;
    background:#fff;
    border: 2px solid #ccc;
    color:#000;
    cursor:pointer;
    font-size:15px;

    &:hover
    {
        background:#ccc;
    }
`
export const Textarea = styled.textarea
`
    margin-bottom:2%;
    width:100%;
    outline:0;
    background:#ccc;

`
