/* eslint-disable react/jsx-no-comment-textnodes */


import React, { Component } from 'react'
import Table from './Table'
import Form from './Form'
import TablePos from './TablePos'
import Ftable from './Ftable'
import './App.css'


class App extends Component {
  testPos = []
  testFinal = []
  testMain = []
  

  state = {
    characters: [],
  }
  
  handleSubmit = (character) => {
    this.setState({ characters: [...this.state.characters, character ] })
    this.testPos=[] // Table of possibles has to be deleted after the choice
  }
  handleSubmitForm = (character) => {
    this.setState({ characters: [...this.state.characters, ] })
  }
  removeCharacterPos = () => {
    const { characters } = this.testPos
  
    this.setTestPos({
      testPos: characters.filter((character, i) => {
        return i =100
      }),
    })
  }

  runModel = async () => {
    
    var average = [];
    const resu = this.state.characters.map((row, index) => {

      average.push(row.energy);
      average.push(row.instrumentalness);
      average.push(row.year);
      average.push(row.popular);
      average.push(row.tempo);
    })
    if (average.length <= 0){
      alert("Final Table is Empty!")
    }
    await fetch('http://127.0.0.1:8000/generate_predictions/?input_usr=' + average)// with parameters // with await we wait until it finishes processing
    .then(response => 
      response.json())
    .then(data => {
      
      for (let i = 0;i<5;i++){
        this.updateFtab(data[i][0],data[i][1],data[i][2],data[i][3])
      }   
    })
    this.setState({ characters: [...this.state.characters, ] })
  }
  
  updatePos = (sartwrk,sName,sArt,album,energy,instru,popul,tempo,year) => {
    this.testPos.push([sartwrk,sName,sArt,album,energy,instru,popul,tempo,year])
  }
  
  updateFtab = (sartwrk,sName,sArt,album) => {
    this.testFinal.push([sartwrk,sName,sArt,album])
  }
  
  removeCharacter = (index) => {
    const { characters } = this.state
  
    this.setState({
      characters: characters.filter((character, i) => {
        return i !== index
      }),
    })
  }

  
  render(){
    const { characters } = this.state
    var  charactersPos  = this.testPos
    var  charactersFinal  = this.testFinal
    
    return(
      
      <div  className="container" align ="center" style={{backgroundColor: "#Fefeff"}}>
      <div>
         <img src="https://www.interstride.com/wp-content/uploads/2022/05/slu_logo.png" alt="React Logo" 
         width = "160px" align = "left" class = "imagslu"/>
         <h1 class = "titles"> Spotify Song Recommendation System</h1>
      </div>
      <h2 > What is a Recommendation System?</h2>
        <h3 class = "texts"> A recommendation System returns us a specific object or idea believed to be of interest.
         We use these recommendation systems in all areas, but until recently, performance was hampered by traditional algorithms
         and their excessive execution time, not compatible with these types of large scale applications. </h3>
         <h3 class = "texts"> We can bypass these constraints by using Machine Learning, and more specifically Neural Networks. Neural Networks
         aim to simulate brain function between interacting neurons. Through models made up of layers of nodes,
         we can estimate a solution to a problem.</h3>
         <div>
         <img  class = "imgdiagram" src="https://datalya.com/blog/content/4-machine-learning/11-machine-learning-vs-traditional-programming-paradigm/ml_vs_traditional_paradigm.png" alt="explication"
         width = "470px" align = "left"/>
         <h3 class = "explnvsa" align = "right"> Neural Networks (NNs) and Machine Learning algorithms differ from traditional algorithms in many ways. In order to find a suitable algorithm 
         using machine learning, we must either let the program define the answer itself (unsupervised training) or train it, supplying the answers ourselves (supervised training).
         Then, the model can be further enhanced by changing hyperparameters, such as; batch size, number of epochs, learning rate and many many more. </h3>
         </div>
         <h2 class = "header2"> Why would we use Neural Networks instead of traditional Algorithms?</h2>
         
         <h3 class = "texts"> As NNs allow us to essentially teach the algorithm how to score, their extreme malleability in the sense that they can emulate the behaviour of 
         most other algorithms and ever-changing nature, meaning that they can always be improved at any step of the way, make NNs and by enlarge, Machine Learning, one of the premier fields 
         in computing today. NNs also outperform most traditional algorithms in execution time, making them very desirable for real time applications. 
         Furthermore, innovations in how NNs are trained and deployed, and new ways of implementing them make the future very promising for this field.  </h3>
         
         <h2 class = "titlemod"> Below we have an example of a Neural Network trained for a Song Recommendation System</h2>
        <div class = "form2" ><Form  handleSubmit={this.handleSubmitForm} upPos = {this.updatePos}></Form></div>
        <h1> </h1>
        <div className ="right-half" >
            <h2 align = "center">  Possible Candidates:</h2>
            <TablePos  width="100%" characterData={charactersPos} handleSubmit={this.handleSubmit} />
            </div>
            <h1> </h1>
        <div className ="left-half"  >
        <h2 align = "center">  Final Track List:</h2>
        <Table width="100%"  characterData={characters} removeCharacter={this.removeCharacter}  />
        </div>
            <h1> </h1>
            <h2> Run the Model (Make sure you have enough songs in the Final Track List!)</h2>
            <div class = "but"><button class = "buttond" type = "button" width="600" height="100" onClick = {this.runModel}> Run the Model!</button></div>
        <div className = "footer">
            <h2 align = "center">  Top 5 Recommendations:</h2>
            <Ftable width="100%"  characterData={charactersFinal}   />
        </div>
        <h1> Limitations and Enhancements</h1>
        <h3 class = "texts"> A lack of accuracy in a given model can be due to numerous factors that can help deceive predictions.
        One such factor can be a lack of distribution either in the training set itself or in the dataset in which the model bases its 
        results. Scores that are under-represented will not be modelled to the same standard than others, and therefore will lead to less
        accurate predictions. Another cause for inaccurate models is over and under-fitting, these can occur when the model bases its generated predictions
        too heavily or not heavily enough on the training or validation sets. Finally, the Neural Network itself, could be too complex or not complex enough, which
        could lead to again, a model which does not perform to the specified characteristics. </h3>
        <h3 class = "texts">Acknowledgements:<br></br>- SLU logo belongs to Saint Louis University<br></br>- Algorithm comparison chart belongs to datalya.com  </h3>
        <h5 align = "left" class = "textskey">Key:<br></br>training set: The set of data values entered into the model.<br></br>dataset: The starting dataset containing all of the tracks used for training.  </h5>
        <h4 align="right" class = "mynameis"> By: Juan Colón de Carvajal León</h4>
        </div>
        
        
    )
  } 
}


export default App;

/*
.explnvsa{
  max-width: 500px;
  margin-left: 50px;
  margin-right: 190px;
  margin-top: 0px;
}
.imgdiagram {
  margin-left: 550px;
}

        <img src="https://drive.google.com/uc?export=view&id=1CdqBk0BsZe7yIhwG2U2kpf3PVAwWR0td" alt="drive image"/>

*/
