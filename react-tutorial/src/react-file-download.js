import React, { Component } from 'react'
import axios,{get} from 'axios';

var fileDownload = require('js-file-download');
class SimpleFileDownload extends Component {

  constructor(props) {
    super(props);

    
    //this.loadData = this.loadData.bind(this)
    this.download = this.download.bind(this)
  }
  

  // componentDidMount() {
  //   this.loadData()
  //   setInterval(this.loadData, 300);
  // }


  // loadData(){

  //   const id = setInterval(download, 3000);
  //   var percent = 0;

  //   function download() {
  //     // fake server request, getting the file url as response
  //     get("http://127.0.0.1:5000/download")
  //     .then( (response) => {
  //       console.log("response", response);
  //       // this.setState({
  //       //   loading: Number(response.data)
  //       // });
  //       percent = Number(response.data)
  //       console.log("loading", percent);
  //     })
  //     .catch( (error) => {
  //       console.log(error);
  //     });  
          
  //     if (percent > 5) {
  //       clearInterval(id);
  //       console.log("Process Done!");
  //     }
  
  //   }
    
  // }

  


  download() {

    const url = `http://127.0.0.1:5000/download`;
    
    axios.get(url).then( (response) => {
      console.log("response", response);

      Object.keys(response.data).forEach(key => {
        console.log(response.data[key]);
        fileDownload(response.data[key].result, response.data[key].filename);
      });

    })
    .catch( (error) => {
      console.log(error);
    })

    
  }
  render() {
    return(
      <button onClick={this.download}>Download Results </button>
    );
  }
}

export default SimpleFileDownload