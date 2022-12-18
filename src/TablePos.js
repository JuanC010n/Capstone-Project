import React, { Component } from 'react'
import './Table.css'
import Form from './Form'
import "./TablePos.css"

const TableBodyPos = (props) => {
  const rowsPos = props.characterData.map((row, index) => {
    
    return (
      <tr key={index}>
          <td><img  width="100%" height="100%" src = {row[0]} /> </td>
          <td>{row[1]}</td>
          <td>{row[2]}</td>
          <td>{row[3]}</td>
          <td><button class = "buttond" onClick={() => props.handleSubmit({sartwrk:row[0],sName:row[1],sArt:row[2],
          album:row[3],energy:row[4],instrumentalness:row[5],
          popular:row[6],tempo:row[7],year:row[8] })}>Submit</button></td>        </tr>
    )
  })

  return <tbody>{rowsPos}</tbody>
}


const TableHeaderPos = () => {
return (
    <thead >
    <tr>
        <th>Artwork </th>
        <th>Song Name </th>
        <th>Artist </th>
        <th>Album Name</th>
    </tr>
    </thead>
)
}

const TablePos = (props) => {
    
const { characterData, handleSubmit } = props

return (
    <table id = "ptable" align="center">
    <TableHeaderPos />
    <TableBodyPos characterData={characterData} handleSubmit={handleSubmit} />
    </table>
)
}

export default TablePos;
