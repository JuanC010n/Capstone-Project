import React, { Component, useState } from 'react'
import { findRenderedDOMComponentWithClass } from 'react-dom/test-utils'
import App from './App'
import './Form.css'
import app from './app.py'

class Form extends Component {
  initialState = {
    sartwrk: "",
    sName: "",
    sArt: "",
    album: ""


  }
  state = this.initialState

  submitForm = async () => {
    // Add user input into a compatible string with spotipy
    var params = ""
    if (this.state.sArt.length !== 0){
      params+= "artist:" + this.state.sArt
    }
    if (this.state.album.length !== 0){
      params+= " album:" + this.state.album
    }
    if (this.state.sName.length !== 0){
      params+= " track:" + this.state.sName
    } // In case the user does not enter some of the song attributes
    if (params.length <= 0){
      alert("No information was submitted! Please try again")
    }
    let varss = params;
    await fetch('http://127.0.0.1:8000/search/?parameters=' + varss)// with parameters // with await we wait until it finishes processing
    .then(response => response.json())
    .then(data => {
      for(let i = 0;i<data.length;i++){
        this.props.upPos(data[i][0],data[i][3],data[i][1],data[i][2],data[i][7],data[i][8],data[i][5],data[i][9],data[i][6])
      }
    })

    // Here we add into the possible table when the form is submitted
    this.props.handleSubmit(this.state)// Button needs to be pressed in order for the table to be updated if commented
    this.setState(this.initialState) 
  }

  handleChange = (event) => {
    const { name, value } = event.target
    this.setState({
      [name]: value,
    })
  }

  render() {
    const { sName, sArt, Album } = this.state;
    return (
      <form align = "fit-content">
        <input
          type="text"
          class ="textbox"
          name="sName"
          id="sName"
          placeholder='Track Name'
          value={sName}
          onChange={this.handleChange} />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input
          type="text"
          class ="textbox"
          name="sArt"
          id="sArt"
          placeholder='Artist'
          value={sArt}
          onChange={this.handleChange} />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input
          type="text"
          class ="textbox"
          name="album"
          placeholder='Album'
          id="album"
          value={Album}
          onChange={this.handleChange} />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input type="button" class = "buttond" value=" Search For Song! " onClick={this.submitForm} />

      </form>
    );
  }
}
export default Form;
