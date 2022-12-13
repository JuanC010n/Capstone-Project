import React, { Component } from 'react'
import './Table.css'

const TableBody = (props) => {
    const rows = props.characterData.map((row, index) => {
      return (
        <tr key={index}>
            <td><img  width="100%" height="100%" src={row.sartwrk} /></td>
            <td>{row.sName}</td>
            <td>{row.sArt}</td>
            <td>{row.album}</td>
            <td><button class = "buttond" onClick={() => props.removeCharacter(index)}>Delete</button></td>
        </tr>
      )
    })
  
    return <tbody>{rows}</tbody>
  }


const TableHeader = () => {
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
const Table = (props) => {
const { characterData, removeCharacter } = props

return (
    <table id = "Final_table" align="center">
    <TableHeader />
    <TableBody characterData={characterData} removeCharacter={removeCharacter} />
    </table>
)
}
export default Table
