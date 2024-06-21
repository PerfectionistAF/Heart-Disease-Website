
import React, { Component } from 'react';
import { Link } from 'react-router-dom'

import Home from './../Home'




class Index extends Component {
  render() {

    const { user } = this.props;
    return (

      <div>
        <Home user={user} />

      </div>
    )
  }
}

export default Index;
