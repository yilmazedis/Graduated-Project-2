import React, { Component } from 'react'
import SimpleReactFileUpload from './react-file-upload.js'
import SimpleFileDownload from './react-file-download'
import SimpleProgressBar from './progress-bar'
import {Container, Row, Col} from 'react-bootstrap'
import axios, {post, get} from 'axios';



class Input extends Component {
  render() {
      return (
        <SimpleReactFileUpload which = {this.props.which}/>
      );
  }
}

var percent = 0;
var id;
class App extends React.Component {

  constructor(props) {
    super(props);

    
    
    this.state = {
      inputListProgram: [],
      inputListInput: [],
      inputListLibrary: [],
      loading: 0
    };
    this.onAddBtnClickProgram = this.onAddBtnClickProgram.bind(this);
    this.onAddBtnClickInput = this.onAddBtnClickInput.bind(this);
    this.onAddBtnClickLibrary = this.onAddBtnClickLibrary.bind(this);

    this.startFormSubmit = this.startFormSubmit.bind(this)
    this.startProcess = this.startProcess.bind(this)
    this.traceProcess = this.traceProcess.bind(this)
    this.stopProcess = this.stopProcess.bind(this)
  }

  stopProcess (){
    clearInterval(id);
  }

  startFormSubmit(e){
    e.preventDefault() // Stop form submit
    const url = `http://127.0.0.1:5000/start`;
    const formData = new FormData();
    formData.append('file','start')
    const config = {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
    axios.post(url, formData,config).then( (response) => {
      console.log("response", response);
      
    })
    .catch( (error) => {
      console.log(error);
    })

    this.startProcess();
  }

  onAddBtnClickProgram(event) {
    const inputListProgram = this.state.inputListProgram;
    this.setState({
      inputListProgram: inputListProgram.concat(<Input which = "program" key={inputListProgram.length} />)
    });
  }

  onAddBtnClickInput(event) {
    const inputListInput = this.state.inputListInput;
    this.setState({
      inputListInput: inputListInput.concat(<Input which = "input" key={inputListInput.length} />)
    });
  }

  onAddBtnClickLibrary(event) {
    const inputListLibrary = this.state.inputListLibrary;
    this.setState({
      inputListLibrary: inputListLibrary.concat(<Input which = "library" key={inputListLibrary.length} />)
    });
  }

  startProcess(){
    percent = 0;
    id = setInterval(this.traceProcess, 100);
    
  }

  traceProcess () {
    // fake server request, getting the file url as response
    get("http://127.0.0.1:5000/process")
    .then( (response) => {
      console.log("response", response);
      
      this.setState({
        loading: Number(response.data)
      })
      percent = Number(response.data)
      console.log("loading", percent);
    })
    .catch( (error) => {
      console.log(error);
    })
        
    if (percent >= 100) {
      clearInterval(id);
      percent = 0
      console.log("Process Done!");
    }}
  
  render () {
  return (
      
    <div>
        <Container>
          <Row>
            <Col> <SimpleProgressBar per = {this.state.loading}/> </Col>
          </Row>
          <Row>
            <Col>
            {/* <FilePond server='http://localhost:8000'/> */}
            <button onClick={this.onAddBtnClickProgram}>Add Program</button>
            {this.state.inputListProgram.map(function(input, index) {
              return input;})}
            </Col>
            <Col>
            {/* <FilePond allowMultiple={true}/> */}
            <button onClick={this.onAddBtnClickInput}>Add Input</button>
            {this.state.inputListInput.map(function(input, index) {
              return input;})}
            </Col>
            <Col>
            {/* <FilePond allowMultiple={true}/> */}
            <button onClick={this.onAddBtnClickLibrary}>Add Library</button>
            {this.state.inputListLibrary.map(function(input, index) {
              return input;})}
            </Col>
          </Row>
          <Row>
          <Col md={{ span: 3, offset: 3 }}></Col>
            <Col md={{ span: 3, offset: 3 }}>
            <form onSubmit= {this.startFormSubmit}>
              <button type="submit">Start</button>
            </form>
            </Col>
          </Row>

          <Row>
            <Col>
            {/* <button onClick={this.startProcess}>Download Results </button> */}
              <SimpleFileDownload/>
            </Col>

            <Col>
              <button onClick={this.stopProcess}>Stop Process </button>
            </Col>

            
          </Row>
        </Container>
    </div>
  )}
  
}

export default App