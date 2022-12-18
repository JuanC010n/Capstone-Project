import React, { Component } from 'react'
import './Table.css'
import Form from './Form'


const TableBodyPos2 = (props) => {
  const rowsPos = props.characterData.map((row, index) => {
    
    return (
      <tr key={index}>
          <td><img  width="100%" height="100%" src = {row[0]} /> </td>
          <td>{row[1]}</td>
          <td>{row[2]}</td>
          <td>{row[3]}</td>
          </tr>
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

const Ftable = (props) => {
    
const {characterData} = props

return (
    <table align="center">
    <TableHeaderPos />
    <TableBodyPos2 characterData={characterData}  />
    </table>
)
}

export default Ftable;

