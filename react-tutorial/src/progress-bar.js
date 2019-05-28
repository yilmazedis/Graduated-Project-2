import React, { Component } from 'react'
import  {ProgressBar} from 'react-bootstrap'



class SimpleProgressBar extends Component {
  render() {    
    return <div> <ProgressBar animated now={this.props.per} label={`${this.props.per}%`} /> </div>
  }
}

export default SimpleProgressBar