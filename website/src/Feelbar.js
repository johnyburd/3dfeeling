import React from 'react'
import { withRouter } from 'react-router-dom'
import './Feelbar.scss'

import { Navbar, Nav } from 'react-bootstrap';
import logo from './3dfeeling_logo.png'

import DarkModeToggle from './Dark';

class Feelbar extends React.Component {

  render () {
      return (
          <Navbar className="Feelbar" fixed="top">
            <Navbar.Brand href="/">
              <img alt="3D Feeling Logo" src={logo} width="30" height="30" className="d-inline-block align-top" />{' '}
              3D Feeling
            </Navbar.Brand>
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="justify-content-end" style={{width: "95%"}}>
                <Nav.Link href="/">Home</Nav.Link>
                <Nav.Link href="/details">Details</Nav.Link>
                <DarkModeToggle />
              </Nav>
            </Navbar.Collapse> 
          </Navbar>
      )
    }
}

export default withRouter(Feelbar);