import React ,{Component} from 'react'
import{Container,  Contactt ,Contacttitle ,Form ,Forminput ,Textarea ,Input,InputEmail,InputExp,InputSubmit,InputText ,Span} from './style.js'
const Contact = () => {
    return(
        <Contactt>
            <Container>
                <Contacttitle> 
                     Drop Me A line
                </Contacttitle>
                <Form action=''>
                    <Forminput>
                        <InputText type='text' placeholder='Your Name'/>
                        <InputEmail type='email' placeholder='Your Email'/>
                    </Forminput>
                    <InputExp className='Sup' type='text'  placeholder='Your Subject'/>
                    <Textarea cols="30" rows="10" placeholder='Your Message'></Textarea>
                    <InputSubmit type='submit' values="send Message"/>
                </Form>
            </Container>
        </Contactt>
    )
} 

export default Contact;