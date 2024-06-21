
import styled from 'styled-components'
import { Link } from 'react-router-dom';

export const Navbarsection = styled.div`
    
    overflow: hidden;
    padding:5px 0;
    position:relative;
    background: #fff;
    border-bottom: 1px solid black;
`
export const Container = styled.div`
    width : 100%;
    margin: auto; 
`

export const Logo = styled.div`
    width:50%;
    float:left;

`


export const LogoText = styled.h2`
    font-size: 30px;
    font-weight: bold;
`


export const Ulist = styled.ul`
    width:50%;
    float:left;
    list-style-type: none;
    padding: 0px;
`

export const ListItem = styled.li`
    display: inline-block;
`

export const Anchor = styled.a`
    display: block;
    color:#222;
    text-decoration: none;
    padding: 10px 15px;
    font-weight: bold;

    &:hover{
        color:#eb5424;
    }
`
export const LINK = styled(Link)`
    display: block;
    color:#222;
    text-decoration: none;
    padding: 10px 15px;
    font-weight: bold;

    &:hover{
        color:#eb5424;
    }
`

